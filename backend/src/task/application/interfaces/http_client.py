import abc

import aiohttp


class IHttpClient(abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def get(cls, url: str, **kwargs) -> aiohttp.ClientResponse: ...

    @classmethod
    @abc.abstractmethod
    async def post(cls, url: str, **kwargs) -> aiohttp.ClientResponse: ...

    @classmethod
    @abc.abstractmethod
    async def put(cls, url: str, **kwargs) -> aiohttp.ClientResponse: ...

    @classmethod
    @abc.abstractmethod
    async def delete(cls, url: str, **kwargs) -> aiohttp.ClientResponse: ...

    @classmethod
    @abc.abstractmethod
    async def patch(cls, url: str, **kwargs) -> aiohttp.ClientResponse: ...
