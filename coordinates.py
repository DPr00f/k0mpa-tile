import asyncio
import sys
import requests
from aiohttp import ClientSession
from pytile import async_login
from datetime import datetime
import os

EMAIL = os.environ.get("TILE_EMAIL")
PASSWORD = os.environ.get("TILE_PASSWORD")
API_PASSWORD = os.environ.get("TILE_API_PASSWORD")
TILE_NAME = "k0mpass"
TILES_TO_FIND = ["iPhone de Carlos", "k0mpass"]
API_URL = os.environ.get("TILE_API_SERVER", "http://127.0.0.1:3000/");

post = False
debug = False

for arg in sys.argv:
    if arg == "--post":
        post = True
    if arg == "--debug":
            debug = True

async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login(EMAIL, PASSWORD, session)

        tiles = await api.async_get_tiles()
        tile_to_find = None
        last_timestamp = 0

        for tile_uuid, tile in tiles.items():
            if  not (tile.name in TILES_TO_FIND):
                continue
            if datetime.timestamp(tile.last_timestamp) > last_timestamp:
                tile_to_find = tile
                last_timestamp = datetime.timestamp(tile.last_timestamp)

        if (tile_to_find):
            if debug:
                print(f"Found tile {tile_to_find.name} at {tile_to_find.latitude}, {tile_to_find.longitude}")
            if (post):
                r = requests.post(API_URL + "api/coordinates", json={'id':TILE_NAME, 'latitude':tile.latitude, 'longitude':tile.longitude}, headers={ 'x-api-password': API_PASSWORD })
                print(r)
                return
            r = requests.put(API_URL + "api/coordinates", json={'id':TILE_NAME, 'latitude':tile.latitude, 'longitude':tile.longitude}, headers={ 'x-api-password': API_PASSWORD })
            print(r)


asyncio.run(main())
