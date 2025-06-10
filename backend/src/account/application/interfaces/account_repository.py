import abc

from src.account.domain.entities import Account, AccountUpdate


class IAccountRepository(abc.ABC):
    @abc.abstractmethod
    async def get_available(self) -> Account: ...

    @abc.abstractmethod
    async def get_list(self) -> list[Account]: ...

    @abc.abstractmethod
    async def update_by_pk(self, pk: int, data: AccountUpdate) -> Account: ...
