from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.base import Base, BaseMixin


class AccountDB(BaseMixin, Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    balacne_left: Mapped[int | None]

    tokens: Mapped[list["AccountTokenDB"]] = relationship(back_populates="account", lazy="selectin", cascade="all,delete")


class AccountTokenDB(BaseMixin, Base):
    __tablename__ = "account_tokens"

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    access_token: Mapped[str]
    session_id: Mapped[str]
    cookies: Mapped[str | None]

    account: Mapped["AccountDB"] = relationship(back_populates="tokens", lazy="noload")
