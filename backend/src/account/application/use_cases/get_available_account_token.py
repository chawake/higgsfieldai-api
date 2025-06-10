from src.db.exceptions import DBModelNotFoundException
from src.account.domain.dtos import AccountTokenDTO
from src.account.domain.exceptions import NoAvailableAccountsException
from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.application.interfaces.auth_client import IAuthClient


class GetAvailableAccountTokenUseCase:
    def __init__(self, uow: IAccountUnitOfWork, auth_client: IAuthClient) -> None:
        self.uow = uow
        self.auth_client = auth_client

    async def execute(self) -> AccountTokenDTO:
        async with self.uow:
            try:
                account = await self.uow.accounts.get_available()
            except DBModelNotFoundException:
                raise NoAvailableAccountsException() from DBModelNotFoundException
        token = account.tokens[0]
        refreshed_token = await self.auth_client.refresh_token(token)
        return AccountTokenDTO(**refreshed_token.model_dump())
