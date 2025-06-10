from src.account.domain.dtos import AccountTokenDTO
from src.account.domain.entities import Token, AccountLogin
from src.integration.domain.exceptions import IntegrationUnauthorizedExeception
from src.account.application.interfaces.auth_client import IAuthClient
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.schemas import ExternalSignInRequest, ExternalSignInResponse


class ExternalAuthClient(IAuthClient):
    def __init__(self) -> None:
        self.external_client = ExternalClient(account_token=None)

    async def login(self, data: AccountLogin) -> Token:
        request = ExternalSignInRequest(identifier=data.username, password=data.password)
        response = await self.external_client.sign_in(request)
        token = self._map_response_to_token(response)
        self.external_client.set_account_token(token)
        await self.external_client.touch_session()
        return Token(**token.model_dump())

    async def refresh_token(self, token: Token) -> Token:
        if not self._refresh_needed(token):
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

    def _map_response_to_token(self, response: ExternalSignInResponse) -> AccountTokenDTO:
        last_active_session = next(
            session for session in response.client.sessions if session.id == response.client.last_active_session_id
        )
        return AccountTokenDTO(
            access_token=last_active_session.last_active_token.jwt,
            session_id=response.response.created_session_id,
            cookies={"__client": response.client_cookie},
        )
