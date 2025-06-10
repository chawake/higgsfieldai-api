from fastapi import Request
from sqladmin import ModelView

from src.account.api.dependencies import get_account_uow
from src.integration.api.dependencies import get_auth_client
from src.account.infrastructure.db.orm import AccountDB
from src.account.application.use_cases.sign_in_account import SignInAccountUseCase


class AccountAdmin(ModelView, model=AccountDB):
    name = "Account"
    column_list = [AccountDB.username, AccountDB.password, AccountDB.created_at]

    async def after_model_change(self, data: dict, model: AccountDB, is_created: bool, request: Request) -> None:
        await SignInAccountUseCase(get_account_uow(), get_auth_client()).execute(model)
