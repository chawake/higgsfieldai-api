from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import async_session_maker
from src.account.application.interfaces.account_uow import IAccountUnitOfWork
from src.account.infrastructure.db.token_repository import PGTokenRepository
from src.account.infrastructure.db.account_repository import PGAccountRepository


class PGAccountUnitOfWork(IAccountUnitOfWork):
    def __init__(self, session_factory=async_session_maker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.accounts = PGAccountRepository(self.session)
        self.tokens = PGTokenRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()
