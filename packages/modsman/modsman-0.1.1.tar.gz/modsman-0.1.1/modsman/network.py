import os
from asyncio import Semaphore
from typing import Dict, Set, List
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests

from modsman.common import Mod

BASE_URL = "https://staging_cursemeta.dries007.net"


# Tried using aiohttp for api requests, but got CERTIFICATE_VERIFY_FAILED.
# The requests lib ships with its own cert bundle, so it works somehow
# TODO make it use async someday


async def get_addons(project_ids: Set[int]) -> List[Mod]:
    if not project_ids:
        return []

    response = requests.get(
        f"{BASE_URL}/api/v3/direct/addon", params=[("id", p) for p in project_ids]
    )
    response.raise_for_status()

    return [Mod(id=a["id"], name=a["name"]) for a in response.json()]


async def get_file_links(project_ids: Set[int], game_version: str) -> Dict[int, str]:
    if not project_ids:
        return dict()

    response = requests.get(
        f"{BASE_URL}/api/v3/direct/addon", params=[("id", p) for p in project_ids]
    )
    response.raise_for_status()

    return {
        addon_data["id"]: max(
            [
                file_data
                for file_data in addon_data["latestFiles"]
                if file_data["isAvailable"]
                if not file_data["isAlternate"]
                if any(game_version in v for v in file_data["gameVersion"])
            ],
            key=lambda f: f["fileDate"],
        )["downloadUrl"]
        for addon_data in response.json()
    }


async def download_file(sem: Semaphore, url: str):
    async with sem:
        file_name = os.path.basename(urlparse(url).path)
        async with aiohttp.request("get", url) as response:
            response.raise_for_status()
            async with aiofiles.open(file_name, mode="wb") as file:
                await file.write(await response.read())
        return file_name
