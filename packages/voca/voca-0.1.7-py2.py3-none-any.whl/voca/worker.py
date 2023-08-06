"""Definition of the worker process.

Each worker is started by the manager. It loads the grammar from the specified
modules matching in the current context, and it executes the received command
before exiting.

The worker sends its logs up to the manager over stdout rather than writing
directly to the log file so the manager can make sure log lines are interleaved
without overlapping in the output.
"""

import importlib
import functools
import sys
import os
import textwrap
import json
import types
import shutil
import pathlib
import importlib.util


from typing import Iterable
from typing import List
from typing import Tuple

import eliot
import trio
import toml
import lark


from voca import utils
from voca import streaming
from voca import log
from voca import parsing
from voca import context
from voca import config


@log.log_async_call
async def handle_message(wrapper_group: utils.WrapperGroup, data: dict):
    """Execute the command in ``data`` with the ``wrapper_group`` containing the grammar."""
    message = data["result"]["hypotheses"][0]["transcript"]

    with eliot.start_action(action_type="parse_command") as action:

        handler = await make_specific_handler(wrapper_group, data)
        tree = handler.parser.parse(message)

    commands = parsing.extract_commands(tree)

    for command in commands:
        rule_name, args = command.data, command.children
        function = handler.rule_name_to_function[rule_name]
        with eliot.start_action(
            action_type="run_command", command=rule_name, args=args, function=function
        ):
            await function(args)


@log.log_call
def load_from_path(import_path: str, filename: str) -> types.ModuleType:
    """Load a module from a filesystem path."""
    spec = importlib.util.spec_from_file_location(import_path, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@log.log_call
def get_backup_module(import_path: str, backup_dir: pathlib.Path) -> types.ModuleType:
    """Import a module from the backup directory."""
    sys.path.insert(0, str(backup_dir))
    try:
        module = importlib.import_module(import_path)
    except Exception:
        module = None
    finally:
        del sys.path[0]
    return module


@log.log_call
def save_backup_module(
    module: types.ModuleType, import_path: str, backup_dir: pathlib.Path
) -> None:
    """Save a module in the backup directory."""
    new_path = (backup_dir / import_path.replace(".", "/")).with_suffix(".py")
    new_path.parent.mkdir(exist_ok=True, parents=True)
    shutil.copy2(module.__file__, new_path)


@log.log_call
def get_module(
    import_path: str, backup_dir: pathlib.Path, use_backup_modules: bool
) -> types.ModuleType:
    """Import module and cache it in backup_dir, returning backup on failure."""

    try:
        with eliot.start_action(
            action_type="import_module",
            import_path=import_path,
            sys_path=sys.path,
            sys_meta_path=sys.meta_path,
        ):
            module = importlib.import_module(import_path)
    except Exception:
        if not use_backup_modules:
            raise
        module = get_backup_module(import_path, backup_dir)
    else:
        save_backup_module(module, import_path, backup_dir)
    return module


@log.log_call
def collect_modules(
    import_paths: Iterable[str], use_backup_modules: bool
) -> List[types.ModuleType]:
    """Collect modules from import paths, optionally defaulting to backup modules on failure."""

    backup_dir = pathlib.Path(config.get_config_dir()) / "backup_modules"

    modules = []
    for import_path in import_paths:
        module = get_module(import_path, backup_dir, use_backup_modules)
        if module is not None:
            modules.append(module)
    return modules


def combine_registries(registries: utils.Registry) -> utils.Registry:
    """Combine multiple registries into a single one."""
    combined = utils.Registry()
    for registry in registries:
        combined.pattern_to_function.update(registry.pattern_to_function)
        combined.patterns.update(registry.patterns)
    return combined


async def make_specific_handler(wrapper_group: utils.WrapperGroup, data: dict):
    """Build the command handler for the specific context."""
    filtered = await context.filter_wrappers(wrapper_group, data)
    registry = combine_registries([wrapper.registry for wrapper in filtered.wrappers])

    rules = parsing.build_rules(registry)
    grammar = parsing.build_grammar(registry, rules)
    rule_name_to_function = {rule.name: rule.function for rule in rules}

    parser = lark.Lark(
        grammar, debug=True, lexer="dynamic_complete", maybe_placeholders=True
    )

    return utils.Handler(
        registry=registry, parser=parser, rule_name_to_function=rule_name_to_function
    )


@log.log_async_call
async def async_main(wrapper_group: utils.WrapperGroup):
    """Process input commands as newline-separated json on stdin."""
    stream = trio._unix_pipes.PipeReceiveStream(os.dup(0))
    receiver = streaming.TerminatedFrameReceiver(stream, b"\n")

    async for message_bytes in receiver:
        data = json.loads(message_bytes.decode())

        try:
            with eliot.Action.continue_task(
                task_id=data.get("eliot_task_id", "@")
            ) as action:
                await handle_message(wrapper_group=wrapper_group, data=data)
        except Exception as e:
            action.finish(e)
            raise

        sys.exit(0)


@utils.public
@log.log_call
def main(import_paths: Tuple[str], use_backup_modules: bool):
    """Get the wrapper group and start the event loop."""

    sys.path.insert(0, str(config.get_config_dir()))
    modules = collect_modules(import_paths, use_backup_modules)
    modules = [utils.transform_module(module) for module in modules]

    wrapper_group = parsing.combine_modules(modules)

    trio.run(functools.partial(async_main, wrapper_group=wrapper_group))
