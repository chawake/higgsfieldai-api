from pydantic import BaseModel

from src.integration.infrastructure.external.schemas import ExternalSignInResponse


class ScrapperLoginResponse(BaseModel):
    response: ExternalSignInResponse
    cookies: dict[str, str]
