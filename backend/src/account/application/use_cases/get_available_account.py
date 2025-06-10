from src.db.exceptions import DBModelNotFoundException
from src.account.domain.dtos import AccountReadDTO
from src.account.domain.entities import Account
from src.account.domain.exceptions import NoAvailableAccountsException
from src.account.application.interfaces.account_uow import IAccountUnitOfWork


class GetAvailableAccountUseCase:
    def __init__(self, uow: IAccountUnitOfWork) -> None:
        self.uow = uow

    async def execute(self) -> AccountReadDTO:
        async with self.uow:
            try:
                account = await self.uow.accounts.get_available()
            except DBModelNotFoundException:
                raise NoAvailableAccountsException() from DBModelNotFoundException
        return self._to_dto(account)

    @staticmethod
    def _to_dto(model: Account) -> AccountReadDTO:
        return AccountReadDTO(**model.model_dump())
