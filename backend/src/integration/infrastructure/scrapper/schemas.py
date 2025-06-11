from pydantic import BaseModel

from src.integration.infrastructure.external.schemas import ExternalSignInResponse


class ScrapperLoginResponse(BaseModel):
    sign_in_response: ExternalSignInResponse
    cookies: dict[str, str]
