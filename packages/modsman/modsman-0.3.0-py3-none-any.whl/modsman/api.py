from typing import Dict, List, Any

import aiofiles
import aiohttp
from aiohttp import request

API_URL = "https://addons-ecs.forgesvc.net/api/"


async def get_addons(project_ids: List[int]) -> List[Dict[str, Any]]:
    async with request("post", API_URL + "addon", json=project_ids) as response:
        response.raise_for_status()
        return await response.json()


async def get_addon_files(project_id: int) -> List[Dict[str, Any]]:
    async with request("get", API_URL + f"addon/{project_id}/files") as response:
        response.raise_for_status()
        return await response.json()


async def match_fingerprints(fingerprints: List[int]) -> Dict[str, Any]:
    async with request("post", API_URL + "fingerprint", json=fingerprints) as response:
        response.raise_for_status()
        return await response.json()


async def download_file(url: str, file_name: str):
    async with aiohttp.request("get", url) as response:
        response.raise_for_status()
        async with aiofiles.open(file_name, mode="wb") as file:
            await file.write(await response.read())
