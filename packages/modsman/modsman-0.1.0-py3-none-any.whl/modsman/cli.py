import argparse
import asyncio
import sys
from typing import List

from modsman.modlist import Modlist


def load_or_fail(file):
    try:
        return Modlist.load(file)
    except FileNotFoundError:
        print(
            f"File '{file}' not found! Did you forget to run `init`?", file=sys.stderr
        )
        sys.exit(1)


async def run_init(file: str, game_version: str):
    modlist = Modlist.init(file, game_version=game_version)
    if modlist is None:
        print(f"File '{file}' already exists!", file=sys.stderr)
        sys.exit(1)
    else:
        modlist.save()
        print(f"Initialized")


async def run_add(file: str, project_ids: List[int]):
    for mod in await load_or_fail(file).add(project_ids):
        print(f"Added '{mod.name}'")


async def run_remove(file: str, project_ids: List[int]):
    for mod in await load_or_fail(file).remove(project_ids):
        print(f"Removed '{mod.name}'")


async def run_remove_all(file: str):
    modlist = load_or_fail(file)
    for mod in await load_or_fail(file).remove(list(modlist.mods.keys())):
        print(f"Removed '{mod.name}'")


async def run_list(file: str):
    for mod in load_or_fail(file).mods.values():
        print(
            f"{mod.name} ({mod.id}) {f'as {mod.installed.file}' if mod.installed  else 'not installed'}"
        )


async def run_install(file: str, num_parallel: int):
    async for mod in load_or_fail(file).gen_install(num_parallel=num_parallel):
        print(f"Downloaded '{mod.name}' as {mod.installed.file}")


async def run_upgrade(file: str, num_parallel: int):
    async for mod in load_or_fail(file).gen_upgrade(num_parallel):
        print(f"Downloaded '{mod.name}' as {mod.installed.file}")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=".modlist.toml")

    subparsers = parser.add_subparsers(required=True)

    init_parser = subparsers.add_parser(name="init")
    init_parser.add_argument("game_version", type=str, metavar="game-version")
    init_parser.set_defaults(function=run_init)

    add_parser = subparsers.add_parser(name="add")
    add_parser.add_argument("project_ids", metavar="project-id", type=int, nargs="+")
    add_parser.set_defaults(function=run_add)

    remove_parser = subparsers.add_parser(name="remove")
    remove_parser.add_argument("project_ids", metavar="project-id", type=int, nargs="+")
    remove_parser.set_defaults(function=run_remove)

    remove_all_parser = subparsers.add_parser(name="remove-all")
    remove_all_parser.set_defaults(function=run_remove_all)

    list_parser = subparsers.add_parser(name="list")
    list_parser.set_defaults(function=run_list)

    install_parser = subparsers.add_parser(name="install")
    install_parser.add_argument("--num-parallel", type=int, default=10)
    install_parser.set_defaults(function=run_install)

    upgrade_parser = subparsers.add_parser(name="upgrade")
    upgrade_parser.add_argument("--num-parallel", type=int, default=10)
    upgrade_parser.set_defaults(function=run_upgrade)

    try:
        args = parser.parse_args()
    except TypeError:
        parser.print_help()
        sys.exit(1)

    asyncio.run(
        args.function(**{k: v for k, v in vars(args).items() if k != "function"})
    )
