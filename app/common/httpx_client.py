import typing

import httpx


class HttpxClient:

    def __init__(self, default_headers: dict = None) -> None:
        self.httpx_client = httpx.AsyncClient(headers=default_headers)

    async def post(self, url: str, json: typing.Any = None, data: dict = None, headers: dict = None):
        async with self.httpx_client as client:
            return await client.post(url=url, json=json, data=data, headers=headers, timeout=None)

    async def get(self, url, headers: dict = None):
        async with self.httpx_client as client:
            return await client.get(url=url, headers=headers, timeout=None)

    async def put(self, url: str, json: typing.Any = None, data: dict = None, headers: dict = None):
        async with self.httpx_client as client:
            return await client.put(url=url, json=json, data=data, headers=headers, timeout=None)
