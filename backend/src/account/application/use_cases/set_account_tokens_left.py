from src.account.domain.entities import AccountUpdate
from src.account.application.interfaces.account_uow import IAccountUnitOfWork


class SetAccountTokensLeftUseCase:
    def __init__(self, uow: IAccountUnitOfWork) -> None:
        self.uow = uow

    async def execute(self, account_id: int, tokens_left: int) -> None:
        async with self.uow:
            await self.uow.accounts.update_by_pk(account_id, AccountUpdate(balance_left=tokens_left))
            await self.uow.commit()
