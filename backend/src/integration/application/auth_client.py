from src.account.domain.dtos import AccountTokenDTO
from src.account.domain.entities import Token, AccountLogin
from src.integration.domain.exceptions import IntegrationUnauthorizedExeception
from src.account.application.interfaces.auth_client import IAuthClient
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.schemas import ExternalSignInRequest, ExternalSignInResponse
from src.integration.infrastructure.scrapper.client import ScrapperClient
from src.integration.infrastructure.scrapper.schemas import ScrapperLoginResponse


class ExternalAuthClient(IAuthClient):
    def __init__(self) -> None:
        self.external_client = ExternalClient(account_token=None)
        self.scrapper_client = ScrapperClient()

    async def login(self, data: AccountLogin) -> Token:
        response = await self.scrapper_client.login(data.username, data.password)
        return self._map_response_to_token(response)

    async def refresh_token(self, token: Token) -> Token:
        if not await self._refresh_needed(token):
            return token

        self.external_client.set_account_token(AccountTokenDTO(**token.model_dump()))
        response = await self.external_client.refresh_token()
        return Token(access_token=response.jwt, session_id=token.session_id, cookies=token.cookies)

    async def _refresh_needed(self, token: Token) -> bool:
        self.external_client.set_account_token(AccountTokenDTO(**token.model_dump()))
        try:
            await self.external_client.get_current_user()
        except IntegrationUnauthorizedExeception:
            return True
        return False

    def _map_response_to_token(self, response: ScrapperLoginResponse) -> Token:
        last_active_session = next(
            session
            for session in response.sign_in_response.client.sessions
            if session.id == response.sign_in_response.client.last_active_session_id
        )
        return Token(
            access_token=last_active_session.last_active_token.jwt,
            session_id=response.sign_in_response.response.created_session_id,
            cookies=response.cookies,
        )
