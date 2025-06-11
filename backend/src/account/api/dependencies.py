from typing import Annotated

from fastapi import Depends

from src.account.application.use_cases.refresh_account_tokens import RefreshAccountTokensUseCase
from src.account.domain.dtos import AccountReadDTO, AccountTokenDTO
from src.integration.api.dependencies import get_auth_client
from src.account.infrastructure.db.unit_of_work import PGAccountUnitOfWork
from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.application.interfaces.auth_client import IAuthClient
from src.account.application.use_cases.get_available_account import GetAvailableAccountUseCase
from src.account.application.use_cases.get_available_account_token import GetAvailableAccountTokenUseCase


def get_account_uow() -> IAccountUnitOfWork:
    return PGAccountUnitOfWork()


AccountUoWDepend = Annotated[IAccountUnitOfWork, Depends(get_account_uow)]
AuthClientDepend = Annotated[IAuthClient, Depends(get_auth_client)]


async def get_available_account(uow: AccountUoWDepend) -> AccountReadDTO:
    return await GetAvailableAccountUseCase(uow).execute()


async def get_available_account_token(uow: AccountUoWDepend, auth_client: AuthClientDepend) -> AccountTokenDTO:
    return await GetAvailableAccountTokenUseCase(uow, auth_client).execute()


def get_account_token_refresher(auth_client: AuthClientDepend) -> RefreshAccountTokensUseCase:
    return RefreshAccountTokensUseCase(auth_client)
