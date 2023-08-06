from typing import NamedTuple


class Installed(NamedTuple):
    url: str
    file: str

    @staticmethod
    def from_dict(data):
        return Installed(**data)

    def to_dict(self):
        return {"url": self.url, "file": self.file}


class Mod(NamedTuple):
    id: int
    name: str
    installed: Installed = None

    @staticmethod
    def from_dict(data):
        if "installed" in data:
            data.update({"installed": Installed.from_dict(data["installed"])})
        return Mod(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "installed": self.installed.to_dict() if self.installed else None,
        }


class Config(NamedTuple):
    game_version: str

    @staticmethod
    def from_dict(data):
        return Config(**data)

    def to_dict(self):
        return {"game_version": self.game_version}
