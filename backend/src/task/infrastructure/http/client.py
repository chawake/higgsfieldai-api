from socket import AF_INET

import aiohttp
from loguru import logger

from src.task.application.interfaces.http_client import IHttpClient

SIZE_POOL_AIOHTTP = 100
CONNECTION_TIMEOUT = 120
logger = logger.bind(name="httpclient")


class AsyncHttpClient(IHttpClient):
    aiohttp_client: aiohttp.ClientSession | None = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=CONNECTION_TIMEOUT)
            connector = aiohttp.TCPConnector(
                family=AF_INET,
                limit_per_host=SIZE_POOL_AIOHTTP,
            )
            cls.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def get(cls, url: str, **kwargs) -> aiohttp.ClientResponse:
        client = cls.get_aiohttp_client()

        logger.debug(f"Started GET {url}")
        response = await client.get(url, **kwargs)
        return response

    @classmethod
    async def post(cls, url: str, **kwargs) -> aiohttp.ClientResponse:
        client = cls.get_aiohttp_client()

        logger.debug(f"Started POST: {url}")
        response = await client.post(url, **kwargs)
        return response

    @classmethod
    async def put(cls, url: str, **kwargs) -> aiohttp.ClientResponse:
        client = cls.get_aiohttp_client()

        logger.debug(f"Started PUT: {url}")
        response = await client.put(url, **kwargs)
        logger.debug(f"Response PUT {url}: {await response.text()}")
        return response

    @classmethod
    async def delete(cls, url: str, **kwargs) -> aiohttp.ClientResponse:
        client = cls.get_aiohttp_client()

        logger.debug(f"Started DELETE: {url}")
        response = await client.delete(url, **kwargs)
        return response

    @classmethod
    async def patch(cls, url: str, **kwargs) -> aiohttp.ClientResponse:
        client = cls.get_aiohttp_client()

        logger.debug(f"Started PATCH: {url}")
        response = await client.patch(url, **kwargs)
        return response
