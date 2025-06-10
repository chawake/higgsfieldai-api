import abc

from src.account.domain.entities import Token, AccountLogin


class IAuthClient(abc.ABC):
    @abc.abstractmethod
    async def login(self, data: AccountLogin) -> Token: ...

    @abc.abstractmethod
    async def refresh_token(self, token: Token) -> Token: ...
