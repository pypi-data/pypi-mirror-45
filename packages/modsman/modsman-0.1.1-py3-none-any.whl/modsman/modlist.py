import asyncio
from asyncio import Semaphore, BoundedSemaphore
from os import PathLike
from typing import NamedTuple, Dict, List, AsyncIterable, Optional

import toml
from pathlib import Path

from modsman.common import Config, Mod, Installed
from modsman.network import get_addons, get_file_links, download_file


class Modlist(NamedTuple):
    path: PathLike
    config: Config
    mods: Dict[int, Mod]

    @staticmethod
    def init(name: str, game_version: str) -> Optional["Modlist"]:
        path = Path(name)
        if path.exists():
            return None
        else:
            return Modlist(path=path, config=Config(game_version=game_version), mods={})

    @staticmethod
    def load(name: str) -> "Modlist":
        path = Path(name)
        with open(path) as file:
            data = toml.load(file)
        return Modlist(
            path=path,
            config=Config.from_dict(data["config"]),
            mods={mod["id"]: Mod.from_dict(mod) for mod in data.get("mods") or []},
        )

    def to_dict(self):
        return {
            "config": self.config.to_dict(),
            "mods": [mod.to_dict() for mod in self.mods.values()],
        }

    def save(self):
        data = self.to_dict()
        with open(self.path, mode="w+") as file:
            toml.dump(data, file)

    async def add(self, project_ids: List[int]) -> List[Mod]:
        project_ids = {p for p in project_ids if p not in self.mods}
        new_mods = await get_addons(project_ids)
        for mod in new_mods:
            self.mods[mod.id] = mod
        self.save()
        return new_mods

    async def remove(self, project_ids: List[int]) -> List[Mod]:
        removed = [
            mod
            for mod in [self.mods.pop(p, None) for p in project_ids]
            if mod is not None
        ]
        for mod in removed:
            if mod.installed:
                path = Path(mod.installed.file)
                if path.exists():
                    path.unlink()
        self.save()
        return list(removed)

    async def _install_single(
        self,
        sem: Semaphore,
        project_id: int,
        file_download_url: str,
        upgrade_from: str = None,
    ) -> Mod:
        if upgrade_from:
            path = Path(upgrade_from)
            if path.exists():
                path.unlink()
        file_name = await download_file(sem, file_download_url)
        self.mods[project_id] = self.mods[project_id]._replace(
            installed=Installed(url=file_download_url, file=file_name)
        )
        return self.mods[project_id]

    async def gen_install(self, num_parallel: int) -> AsyncIterable[Mod]:
        ids_to_urls = await get_file_links(
            project_ids={mod.id for mod in self.mods.values() if not mod.installed},
            game_version=self.config.game_version,
        )

        sem = BoundedSemaphore(num_parallel)

        for future_mod in asyncio.as_completed(
            [
                self._install_single(sem, project_id, file_download_url)
                for project_id, file_download_url in ids_to_urls.items()
            ]
        ):
            # noinspection PyUnresolvedReferences
            yield await future_mod

        self.save()

    async def gen_upgrade(self, num_parallel: int) -> AsyncIterable[Mod]:
        ids_to_urls = await get_file_links(
            project_ids={mod.id for mod in self.mods.values() if mod.installed},
            game_version=self.config.game_version,
        )

        to_upgrade = [
            (project_id, self.mods[project_id].installed.file, file_download_url)
            for project_id, file_download_url in ids_to_urls.items()
            if self.mods[project_id].installed
            and self.mods[project_id].installed.url != file_download_url
        ]

        sem = BoundedSemaphore(num_parallel)

        for future_mod in asyncio.as_completed(
            [
                self._install_single(sem, project_id, new_url, upgrade_from=old_file)
                for project_id, old_file, new_url in to_upgrade
            ]
        ):
            # noinspection PyUnresolvedReferences
            yield await future_mod

        self.save()
