import asyncio
from asyncio import BoundedSemaphore
from pathlib import Path
from typing import List, Dict, Any, NamedTuple

import aiofiles
import pyhash

from modsman import api
from modsman.common import Mod
from modsman.modlist import Modlist


class Modsman(NamedTuple):
    modlist: Modlist
    max_concurrent: int = None

    @staticmethod
    async def fingerprint(jar_name: str) -> int:
        async with aiofiles.open(jar_name, "rb") as file:
            data = await file.read()
        data = bytes([b for b in data if b not in (9, 10, 13, 32)])
        hasher = pyhash.murmur2_32()
        return hasher(data, seed=1)

    @staticmethod
    def delete_mod_if_exists(mod: Mod) -> bool:
        path = Path(mod.file_name)
        if path.exists():
            path.unlink()
            return True
        return False

    def choose_best_file(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        return max(
            [
                file
                for file in files
                if file["isAvailable"]
                and not file["isAlternate"]
                and any(
                    self.modlist.config.game_version in version
                    for version in file["gameVersion"]
                )
            ],
            key=lambda file: file["fileDate"],
        )

    async def add_and_download_mod(self, addon: Dict[str, Any], sem: BoundedSemaphore):
        async with sem:
            file = self.choose_best_file(await api.get_addon_files(addon["id"]))
            mod = Mod(
                project_id=addon["id"],
                project_name=addon["name"],
                file_id=file["id"],
                file_name=file["fileNameOnDisk"],
            )
            await api.download_file(url=file["downloadUrl"], file_name=mod.file_name)
            self.modlist.add_or_update(mod)
            return mod

    async def upgrade_mod(self, mod: Mod, sem: BoundedSemaphore):
        async with sem:
            file = self.choose_best_file(await api.get_addon_files(mod.project_id))
            if mod.file_id != file["id"]:
                self.delete_mod_if_exists(mod)
                mod = mod._replace(file_id=file["id"], file_name=file["fileNameOnDisk"])
                await api.download_file(
                    url=file["downloadUrl"], file_name=mod.file_name
                )
                self.modlist.add_or_update(mod)
                return mod, True
            else:
                return mod, False

    async def add_and_download_mods(self, project_ids: List[int]):
        sem = BoundedSemaphore(self.max_concurrent)
        for mod in asyncio.as_completed(
            [
                self.add_and_download_mod(addon, sem)
                for addon in await api.get_addons(project_ids)
            ]
        ):
            # noinspection PyUnresolvedReferences
            yield await mod

    async def upgrade_mods(self):
        sem = BoundedSemaphore(self.max_concurrent)
        for result in asyncio.as_completed(
            [self.upgrade_mod(mod, sem) for mod in self.modlist.mods.values()]
        ):
            # noinspection PyUnresolvedReferences
            yield await result

    async def remove_mods(self, project_ids: List[int]):
        for mod in [self.modlist.remove(project_id) for project_id in project_ids]:
            if mod is not None:
                self.delete_mod_if_exists(mod)
                yield mod

    async def match_mods(self, jars: List[str]):
        fingerprint_to_jar = {await self.fingerprint(jar): jar for jar in jars}
        match_result = await api.match_fingerprints(list(fingerprint_to_jar.keys()))
        id_to_file = {
            match["id"]: match["file"] for match in match_result["exactMatches"]
        }
        id_to_addon = {
            addon["id"]: addon
            for addon in await api.get_addons(list(id_to_file.keys()))
        }
        for project_id in id_to_addon.keys():
            addon = id_to_addon[project_id]
            file = id_to_file[project_id]
            mod = Mod(
                project_id=project_id,
                project_name=addon["name"],
                file_id=file["id"],
                file_name=fingerprint_to_jar[file["packageFingerprint"]],
            )
            self.modlist.add_or_update(mod)
            yield mod
