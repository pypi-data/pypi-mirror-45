import argparse
import asyncio
import sys
from typing import List

from modsman.modlist import Modlist
from modsman.modsman import Modsman

MAX_CONCURRENT = 10


def error(message: str):
    print(message, file=sys.stderr)
    sys.exit(1)


def load_or_fail(file):
    try:
        return Modlist.load(file)
    except FileNotFoundError:
        error(f"File '{file}' not found! Did you forget to run `modsman init`?")


async def run_init(file: str, game_version: str):
    with Modlist.init(file, game_version=game_version) as modlist:
        if modlist is None:
            error(f"Can't init because file '{file}' already exists!")
        else:
            modlist.save()
            print(f"Initialized.")


async def run_add(file: str, project_ids: List[int], max_concurrent: int):
    with load_or_fail(file) as modlist:
        async for mod in Modsman(modlist, max_concurrent).add_and_download_mods(
            project_ids
        ):
            print(f"Downloaded '{mod.project_name}' as '{mod.file_name}'")


async def run_remove(file: str, project_ids: List[int]):
    with load_or_fail(file) as modlist:
        async for mod in Modsman(modlist).remove_mods(project_ids):
            print(f"Deleted '{mod.file_name}'")


async def run_remove_all(file: str):
    with load_or_fail(file) as modlist:
        async for mod in Modsman(modlist).remove_mods(list(modlist.mods.keys())):
            print(f"Deleted '{mod.file_name}'")


async def run_list(file: str):
    for mod in load_or_fail(file).mods.values():
        print(f"{mod.project_id}: '{mod.project_name}' as '{mod.file_name}'")


async def run_upgrade(file: str, max_concurrent: int):
    with load_or_fail(file) as modlist:
        async for mod, upgraded in Modsman(modlist, max_concurrent).upgrade_mods():
            if upgraded:
                print(f"Upgraded '{mod.project_name}' to '{mod.file_name}'")
            else:
                print(f"Mod '{mod.project_name}' is already up to date")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=".modlist.json")

    subparsers = parser.add_subparsers(required=True)

    init_parser = subparsers.add_parser(name="init")
    init_parser.add_argument("game_version", type=str, metavar="game-version")
    init_parser.set_defaults(function=run_init)

    add_parser = subparsers.add_parser(name="add")
    add_parser.add_argument("project_ids", metavar="project-id", type=int, nargs="+")
    add_parser.add_argument("--max-concurrent", type=int, default=MAX_CONCURRENT)
    add_parser.set_defaults(function=run_add)

    remove_parser = subparsers.add_parser(name="remove")
    remove_parser.add_argument("project_ids", metavar="project-id", type=int, nargs="+")
    remove_parser.set_defaults(function=run_remove)

    remove_all_parser = subparsers.add_parser(name="remove-all")
    remove_all_parser.set_defaults(function=run_remove_all)

    list_parser = subparsers.add_parser(name="list")
    list_parser.set_defaults(function=run_list)

    upgrade_parser = subparsers.add_parser(name="upgrade")
    upgrade_parser.add_argument("--max-concurrent", type=int, default=MAX_CONCURRENT)
    upgrade_parser.set_defaults(function=run_upgrade)

    try:
        args = parser.parse_args()
    except TypeError:
        parser.print_help()
        sys.exit(1)

    asyncio.run(
        args.function(**{k: v for k, v in vars(args).items() if k != "function"})
    )
