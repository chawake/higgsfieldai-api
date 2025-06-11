from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    session_id: str
    cookies: dict[str, str] | None = None


class Account(BaseModel):
    id: int
    username: str
    balance_left: int | None = None
    tokens: list[Token]


class AccountUpdate(BaseModel):
    balance_left: int | None = None


class AccountLogin(BaseModel):
    username: str
    password: str


class TokenCreate(BaseModel):
    access_token: str
    session_id: str
    account_id: int
    cookies: str | None = None
