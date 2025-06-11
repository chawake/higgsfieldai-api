from pydantic import ValidationError
from src.integration.application.interfaces.http_client import IHttpClient
from src.integration.domain.exceptions import IntegrationRequestException
from src.integration.infrastructure.http.api import HttpApiClient
from src.integration.infrastructure.http.client import AsyncHttpClient
from src.integration.infrastructure.scrapper.schemas import ScrapperLoginResponse
from src.core.config import settings


class ScrapperClient(HttpApiClient):
    def __init__(
        self,
        client: IHttpClient = AsyncHttpClient(),
        source_url: str = settings.SCRAPPER_API_URL,
    ):
        super().__init__(client, source_url)

    async def login(self, username: str, password: str) -> ScrapperLoginResponse:
        response = await self.request("POST", "/login", json={"username": username, "password": password})
        try:
            return ScrapperLoginResponse.model_validate(response.data)
        except ValidationError as e:
            raise IntegrationRequestException(str(e)) from e
