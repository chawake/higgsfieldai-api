import json

from sqlalchemy import or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions import DBModelConflictException, DBModelNotFoundException
from src.account.domain.entities import Token, Account, AccountUpdate
from src.account.infrastructure.db.orm import AccountDB
from src.account.application.interfaces.account_repository import IAccountRepository


class PGAccountRepository(IAccountRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e.orig)
            raise DBModelConflictException(detail) from e

    async def get_available(self) -> Account:
        query = (
            select(AccountDB)
            .options(selectinload(AccountDB.tokens))
            .filter(or_(AccountDB.balacne_left > 0, AccountDB.balacne_left == None))
        )
        models = await self.session.scalars(query)
        model = models.one_or_none()
        if model is None:
            raise DBModelNotFoundException()
        return self._to_domain(model)

    async def get_list(self) -> list[Account]:
        query = select(AccountDB).options(selectinload(AccountDB.tokens))
        models = await self.session.scalars(query)
        return [self._to_domain(model) for model in models]

    async def get_by_pk(self, pk: int) -> Account:
        model = await self.session.get(AccountDB, pk)
        if model is None:
            raise DBModelNotFoundException()
        return self._to_domain(model)

    async def update_by_pk(self, pk: int, data: AccountUpdate) -> Account:
        query = update(AccountDB).values(**data.model_dump(exclude_unset=True)).filter_by(id=pk)
        await self.session.execute(query)
        await self._flush()
        return await self.get_by_pk(pk)

    @staticmethod
    def _to_domain(model: AccountDB) -> Account:
        return Account(
            id=model.id,
            username=model.username,
            balance_left=model.balacne_left,
            tokens=[
                Token(
                    access_token=token.access_token,
                    session_id=token.session_id,
                    cookies=json.loads(token.cookies) if token.cookies else None,
                )
                for token in model.tokens
            ],
        )
