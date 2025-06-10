from src.account.domain.dtos import AccountTokenDTO
from src.integration.infrastructure.external.entities import ExternalAuthData


class AccountTokenDTOToExternalAuthDataMapper:
    def map_one(self, dto: AccountTokenDTO) -> ExternalAuthData:
        return ExternalAuthData(
            session_id=dto.session_id, access_token=dto.access_token, client_cookie=self._extract_client_cookie(dto)
        )

    @staticmethod
    def _extract_client_cookie(dto: AccountTokenDTO) -> str:
        if dto.cookies and "__client" in dto.cookies:
            return dto.cookies["__client"]
        raise ValueError(f"Failed to map account token: Cookies is invalid {dto.cookies}")
