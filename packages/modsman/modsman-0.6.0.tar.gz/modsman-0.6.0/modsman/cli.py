import argparse
import asyncio
import sys
from typing import List

import pkg_resources

from modsman.modlist import Modlist
from modsman.modsman import Modsman


def error(message: str):
    print(message, file=sys.stderr)
    sys.exit(1)


def load_or_fail(mod_list_file):
    try:
        return Modlist.load(mod_list_file)
    except FileNotFoundError:
        error(
            f"File '{mod_list_file}' not found! Did you forget to run `modsman init`?"
        )


async def run_init(mod_list_file: str, game_version: str):
    modlist = Modlist.init(mod_list_file, game_version=game_version)
    if modlist is None:
        error(f"Can't init because file '{mod_list_file}' already exists!")
    modlist.save()
    print(f"Initialized.")


async def run_add(mod_list_file: str, project_ids: List[int], max_concurrent: int):
    with load_or_fail(mod_list_file) as modlist:
        async for mod in Modsman(modlist, max_concurrent).add_and_download_mods(
            project_ids
        ):
            print(f"Downloaded '{mod.project_name}' as '{mod.file_name}'")


async def run_remove(mod_list_file: str, project_ids: List[int]):
    with load_or_fail(mod_list_file) as modlist:
        async for mod in Modsman(modlist).remove_mods(project_ids):
            print(f"Deleted '{mod.file_name}'")


async def run_upgrade(mod_list_file: str, project_ids: List[int], max_concurrent: int):
    with load_or_fail(mod_list_file) as modlist:
        async for mod, upgraded in Modsman(modlist, max_concurrent).upgrade_mods(
            project_ids
        ):
            if upgraded:
                print(f"Upgraded '{mod.project_name}' to '{mod.file_name}'")
            else:
                print(f"Mod '{mod.project_name}' is already up to date")


async def run_reinstall(
    mod_list_file: str, project_ids: List[int], max_concurrent: int
):
    with load_or_fail(mod_list_file) as modlist:
        async for mod in Modsman(modlist, max_concurrent).reinstall_mods(project_ids):
            print(f"Downloaded '{mod.project_name}' as '{mod.file_name}'")


async def run_remove_all(mod_list_file: str):
    await run_remove(
        mod_list_file=mod_list_file,
        project_ids=list(load_or_fail(mod_list_file).mods.keys()),
    )


async def run_upgrade_all(mod_list_file: str, max_concurrent: int):
    await run_upgrade(
        mod_list_file=mod_list_file,
        project_ids=list(load_or_fail(mod_list_file).mods.keys()),
        max_concurrent=max_concurrent,
    )


async def run_reinstall_all(mod_list_file: str, max_concurrent: int):
    await run_reinstall(
        mod_list_file=mod_list_file,
        project_ids=list(load_or_fail(mod_list_file).mods.keys()),
        max_concurrent=max_concurrent,
    )


async def run_discover(mod_list_file: str, jars: List[str]):
    with load_or_fail(mod_list_file) as modlist:
        async for mod in Modsman(modlist).match_mods(jars):
            print(f"Matched '{mod.file_name}' to '{mod.project_name}'")


async def run_list(mod_list_file: str):
    with load_or_fail(mod_list_file) as modlist:
        for mod in modlist.mods.values():
            print(f"{mod.project_id}: '{mod.project_name}' as '{mod.file_name}'")


async def run_list_outdated(mod_list_file: str):
    with load_or_fail(mod_list_file) as modlist:
        async for mod, upgraded in Modsman(modlist).upgrade_mods(
            list(modlist.mods.keys()), dry_run=True
        ):
            if upgraded:
                print(f"{mod.project_id}: '{mod.project_name}' can be updated to '{mod.file_name}'")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=pkg_resources.get_distribution("modsman").version,
    )
    parser.add_argument(
        "--mod-list-file",
        metavar="FILE",
        type=str,
        default=".modlist.json",
        help="alternate .modlist.json",
    )

    subparsers = parser.add_subparsers(required=True)

    init_parser = subparsers.add_parser(name="init", help="initialize a new mod list")
    init_parser.add_argument("game_version", type=str, metavar="GAME_VERSION")
    init_parser.set_defaults(function=run_init)

    add_parser = subparsers.add_parser(name="add", help="download one or more mods")
    add_parser.set_defaults(function=run_add)

    remove_parser = subparsers.add_parser(name="remove", help="delete one or more mods")
    remove_parser.set_defaults(function=run_remove)

    upgrade_parser = subparsers.add_parser(
        name="upgrade", help="update one or more mods"
    )
    upgrade_parser.set_defaults(function=run_upgrade)

    reinstall_parser = subparsers.add_parser(
        name="reinstall", help="force download one or more mods"
    )
    reinstall_parser.set_defaults(function=run_reinstall)

    upgrade_all_parser = subparsers.add_parser(
        name="upgrade-all", help="update all mods in the mod list"
    )
    upgrade_all_parser.set_defaults(function=run_upgrade_all)

    remove_all_parser = subparsers.add_parser(
        name="remove-all", help="delete all mods in the mod list"
    )
    remove_all_parser.set_defaults(function=run_remove_all)

    reinstall_all_parser = subparsers.add_parser(
        name="reinstall-all", help="force download all mods in the mod list"
    )
    reinstall_all_parser.set_defaults(function=run_reinstall_all)

    discover_parser = subparsers.add_parser(
        name="discover", help="add existing jars to the mod list"
    )
    discover_parser.add_argument("jars", metavar="JAR", type=str, nargs="+")
    discover_parser.set_defaults(function=run_discover)

    list_parser = subparsers.add_parser(
        name="list", help="print the mod list to stdout"
    )
    list_parser.set_defaults(function=run_list)

    list_outdated_parser = subparsers.add_parser(
        name="list-outdated", help="list the mods that can be upgraded"
    )
    list_outdated_parser.set_defaults(function=run_list_outdated)

    # add all project-ids args
    for sub in [add_parser, remove_parser, upgrade_parser, reinstall_parser]:
        sub.add_argument(
            "project_ids",
            metavar="PROJECT_ID",
            type=int,
            nargs="+",
            help="one or more CurseForge project ids",
        )

    # add all max-concurrent args
    for sub in [
        add_parser,
        upgrade_parser,
        reinstall_parser,
        upgrade_all_parser,
        reinstall_all_parser,
    ]:
        sub.add_argument(
            "--max-concurrent",
            type=int,
            required=False,
            metavar="N",
            help="the max number of mods to download concurrently",
        )

    try:
        args = parser.parse_args()
    except TypeError:
        parser.print_help()
        sys.exit(1)

    asyncio.run(
        args.function(**{k: v for k, v in vars(args).items() if k != "function"})
    )
