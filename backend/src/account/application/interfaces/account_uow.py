import abc

from src.account.application.interfaces.token_repository import ITokenRepository
from src.account.application.interfaces.account_repository import IAccountRepository


class IAccountUnitOfWork(abc.ABC):
    accounts: IAccountRepository
    tokens: ITokenRepository

    async def commit(self):
        return await self._commit()

    @abc.abstractmethod
    async def _commit(self): ...

    @abc.abstractmethod
    async def _rollback(self): ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._rollback()
