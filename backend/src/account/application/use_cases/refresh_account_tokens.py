from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.application.interfaces.auth_client import IAuthClient
from src.account.domain.dtos import AccountTokenDTO
from src.account.domain.entities import Token


class RefreshAccountTokensUseCase:
    def __init__(self, auth_client: IAuthClient) -> None:
        self.auth_client = auth_client

    async def execute(self, token: AccountTokenDTO) -> AccountTokenDTO:
        refreshed_token = await self.auth_client.refresh_token(Token(**token.model_dump()))
        return AccountTokenDTO(**refreshed_token.model_dump())

