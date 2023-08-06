import json
from os import PathLike
from pathlib import Path
from typing import NamedTuple, Dict, Optional

from modsman.common import Config, Mod


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
            data = json.load(file)
        return Modlist(
            path=path,
            config=Config.from_dict(data["config"]),
            mods={
                mod["project_id"]: Mod.from_dict(mod) for mod in data.get("mods") or []
            },
        )

    def __enter__(self) -> "Modlist":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def to_dict(self):
        return {
            "config": self.config.to_dict(),
            "mods": [mod.to_dict() for mod in self.mods.values()],
        }

    def save(self):
        data = self.to_dict()
        with open(self.path, mode="w+") as file:
            json.dump(data, file, indent=4)

    def add_or_update(self, mod: Mod):
        self.mods[mod.project_id] = mod

    def remove(self, project_id: int):
        return self.mods.pop(project_id, None)

    def update_installed(self, project_id: int, file_id: int, file_name: str):
        self.mods[project_id] = self.mods[project_id]._replace(
            file_id=file_id, file_name=file_name
        )
