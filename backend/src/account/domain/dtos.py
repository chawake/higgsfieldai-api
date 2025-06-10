from pydantic import BaseModel


class AccountReadDTO(BaseModel):
    id: int
    username: str
    tokens_left: int | None = None


class AccountTokenDTO(BaseModel):
    access_token: str
    session_id: str
    cookies: dict[str, str] | None = None
