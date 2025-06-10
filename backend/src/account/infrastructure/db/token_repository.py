import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions import DBModelNotFoundException
from src.account.domain.entities import Token, TokenCreate
from src.account.infrastructure.db.orm import AccountTokenDB
from src.account.application.interfaces.token_repository import ITokenRepository


class PGTokenRepository(ITokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _flush(self):
        try:
            await self.session.flush()
        except IntegrityError as e:
            detail = "Model can't be created. " + str(e.orig)
            raise DBModelNotFoundException(detail) from e

    async def create(self, data: TokenCreate) -> Token:
        model = AccountTokenDB(**data.model_dump(exclude_unset=True))
        self.session.add(model)
        await self._flush()
        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: AccountTokenDB) -> Token:
        return Token(
            access_token=model.access_token,
            session_id=model.session_id,
            cookies=json.loads(model.cookies) if model.cookies else None,
        )
