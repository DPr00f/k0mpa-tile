import asyncio
import sys
import requests
from aiohttp import ClientSession
from pytile import async_login
import os

EMAIL = os.environ.get("TILE_EMAIL")
PASSWORD = os.environ.get("TILE_PASSWORD")
API_PASSWORD = os.environ.get("TILE_API_PASSWORD")
TILE_NAME = "k0mpass"
API_URL = os.environ.get("TILE_API_SERVER", "http://127.0.0.1:3000/");

post = False

for arg in sys.argv:
    if arg == "--post":
        post = True

async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        api = await async_login(EMAIL, PASSWORD, session)

        tiles = await api.async_get_tiles()

        for tile_uuid, tile in tiles.items():
            if tile.name != TILE_NAME:
                break
            if (post):
                r = requests.post(API_URL + "api/coordinates", json={'id':tile.name, 'latitude':tile.latitude, 'longitude':tile.longitude}, headers={ 'x-api-password': API_PASSWORD })
                print(r)
                break
            r = requests.put(API_URL + "api/coordinates", json={'id':tile.name, 'latitude':tile.latitude, 'longitude':tile.longitude}, headers={ 'x-api-password': API_PASSWORD })
            print(r)


asyncio.run(main())
