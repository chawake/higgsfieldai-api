from src.account.domain.dtos import AccountTokenDTO
from src.account.domain.entities import TokenCreate, AccountLogin
from src.account.infrastructure.db.orm import AccountDB
from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.application.interfaces.auth_client import IAuthClient


class SignInAccountUseCase:
    def __init__(self, uow: IAccountUnitOfWork, auth_client: IAuthClient) -> None:
        self.auth_client = auth_client
        self.uow = uow

    async def execute(self, account: AccountDB) -> AccountTokenDTO:
        token = await self.auth_client.login(AccountLogin(username=account.username, password=account.password))
        async with self.uow:
            await self.uow.tokens.create(TokenCreate(**token.model_dump(), account_id=account.id))
            await self.uow.commit()
        return AccountTokenDTO(**token.model_dump())
