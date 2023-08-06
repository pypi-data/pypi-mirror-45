import argparse
import asyncio
import sys
from typing import List

import pkg_resources

from modsman.modlist import Modlist
from modsman.modsman import Modsman

MAX_CONCURRENT = 10


def error(message: str):
    print(message, file=sys.stderr)
    sys.exit(1)


def load_or_fail(mod_list):
    try:
        return Modlist.load(mod_list)
    except FileNotFoundError:
        error(f"File '{mod_list}' not found! Did you forget to run `modsman init`?")


async def run_init(mod_list: str, game_version: str):
    with Modlist.init(mod_list, game_version=game_version) as modlist:
        if modlist is None:
            error(f"Can't init because file '{mod_list}' already exists!")
        else:
            modlist.save()
            print(f"Initialized.")


async def run_add(mod_list: str, project_ids: List[int], max_concurrent: int):
    with load_or_fail(mod_list) as modlist:
        async for mod in Modsman(modlist, max_concurrent).add_and_download_mods(
            project_ids
        ):
            print(f"Downloaded '{mod.project_name}' as '{mod.file_name}'")


async def run_remove(mod_list: str, project_ids: List[int]):
    with load_or_fail(mod_list) as modlist:
        async for mod in Modsman(modlist).remove_mods(project_ids):
            print(f"Deleted '{mod.file_name}'")


async def run_remove_all(mod_list: str):
    with load_or_fail(mod_list) as modlist:
        async for mod in Modsman(modlist).remove_mods(list(modlist.mods.keys())):
            print(f"Deleted '{mod.file_name}'")


async def run_list(mod_list: str):
    with load_or_fail(mod_list) as modlist:
        for mod in modlist.mods.values():
            print(f"{mod.project_id}: '{mod.project_name}' as '{mod.file_name}'")


async def run_upgrade(mod_list: str, max_concurrent: int):
    with load_or_fail(mod_list) as modlist:
        async for mod, upgraded in Modsman(modlist, max_concurrent).upgrade_mods():
            if upgraded:
                print(f"Upgraded '{mod.project_name}' to '{mod.file_name}'")
            else:
                print(f"Mod '{mod.project_name}' is already up to date")


async def run_discover(mod_list: str, jars: List[str]):
    with load_or_fail(mod_list) as modlist:
        async for mod in Modsman(modlist).match_mods(jars):
            print(f"Matched '{mod.file_name}' to '{mod.project_name}'")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=pkg_resources.get_distribution("modsman").version,
    )
    parser.add_argument("--mod-list", metavar="FILE", type=str, default=".modlist.json")

    subparsers = parser.add_subparsers(required=True)

    init_parser = subparsers.add_parser(name="init")
    init_parser.add_argument("game_version", type=str, metavar="game-version")
    init_parser.set_defaults(function=run_init)

    add_parser = subparsers.add_parser(name="add")
    add_parser.add_argument("project_ids", metavar="project-id", type=int, nargs="+")
    add_parser.add_argument("--max-concurrent", type=int, default=MAX_CONCURRENT)
    add_parser.set_defaults(function=run_add)

    remove_parser = subparsers.add_parser(name="remove")
    remove_parser.add_argument("project_ids", metavar="ID", type=int, nargs="+")
    remove_parser.set_defaults(function=run_remove)

    remove_all_parser = subparsers.add_parser(name="remove-all")
    remove_all_parser.set_defaults(function=run_remove_all)

    list_parser = subparsers.add_parser(name="list")
    list_parser.set_defaults(function=run_list)

    upgrade_parser = subparsers.add_parser(name="upgrade")
    upgrade_parser.add_argument("--max-concurrent", type=int, default=MAX_CONCURRENT)
    upgrade_parser.set_defaults(function=run_upgrade)

    discover_parser = subparsers.add_parser(name="discover")
    discover_parser.add_argument("jars", metavar="JAR", type=str, nargs="+")
    discover_parser.set_defaults(function=run_discover)

    try:
        args = parser.parse_args()
    except TypeError:
        parser.print_help()
        sys.exit(1)

    asyncio.run(
        args.function(**{k: v for k, v in vars(args).items() if k != "function"})
    )
