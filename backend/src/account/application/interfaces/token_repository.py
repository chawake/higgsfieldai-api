import abc
from contextvars import Token

from src.account.domain.entities import TokenCreate


class ITokenRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, data: TokenCreate) -> Token: ...
