from typing import NamedTuple


class Mod(NamedTuple):
    project_id: int
    project_name: str
    file_id: int
    file_name: str

    @staticmethod
    def from_dict(data):
        return Mod(**data)

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "file_id": self.file_id,
            "file_name": self.file_name,
        }


class Config(NamedTuple):
    game_version: str

    @staticmethod
    def from_dict(data):
        return Config(**data)

    def to_dict(self):
        return {"game_version": self.game_version}
