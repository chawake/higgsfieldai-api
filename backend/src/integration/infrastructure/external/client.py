from io import BytesIO
from loguru import logger
from typing import Type, TypeVar
from urllib.parse import quote_plus
from contextlib import suppress

from pydantic import BaseModel, ValidationError

from src.account.domain.dtos import AccountTokenDTO
from src.integration.domain.mappers import AccountTokenDTOToExternalAuthDataMapper
from src.integration.domain.exceptions import IntegrationRequestException, IntegrationInvalidResponseException
from src.integration.infrastructure.http.api import HttpApiClient
from src.integration.infrastructure.http.client import AsyncHttpClient
from src.integration.infrastructure.external.schemas import (
    ExternalSignInRequest,
    ExternalSignInResponse,
    ExternalGetUserResponse,
    ExternalGetMotionsRequest,
    ExternalGetMotionsResponse,
    ExternalTouchSessionResponse,
    ExternalCreateMediaLinkResponse,
    ExternalImage2VideoGenerationRequest,
    ExternalImage2VideoGenerationResponse,
)
from src.integration.infrastructure.external.entities import (
    ExternalToken,
    ExternalJobSet,
)

T = TypeVar("T", bound=BaseModel)


class ExternalClient:
    def __init__(self, account_token: AccountTokenDTO | None) -> None:
        self.auth_data = None
        if account_token is not None:
            self.auth_data = AccountTokenDTOToExternalAuthDataMapper().map_one(account_token)

        self.clerk_api = HttpApiClient(
            AsyncHttpClient(),
            source_url="https://clerk.higgsfield.ai",
            cookies={"__client": self.auth_data.client_cookie} if self.auth_data else None,
        )
        self.fnf_api = HttpApiClient(
            AsyncHttpClient(),
            source_url="https://fnf.higgsfield.ai",
            token=self.auth_data.access_token if self.auth_data else None,
        )
        self.http_client = AsyncHttpClient()

    @staticmethod
    def _validate_response[T](response: dict, model: Type[T]) -> T:
        try:
            result = model.model_validate(response)
        except ValidationError as e:
            raise IntegrationInvalidResponseException(e) from e
        return result

    def set_account_token(self, account_token: AccountTokenDTO):
        self.auth_data = AccountTokenDTOToExternalAuthDataMapper().map_one(account_token)
        self.clerk_api = HttpApiClient(
            AsyncHttpClient(),
            source_url="https://clerk.higgsfield.ai",
            cookies={"__client": self.auth_data.client_cookie} if self.auth_data else None,
        )
        self.fnf_api = HttpApiClient(
            AsyncHttpClient(),
            source_url="https://fnf.higgsfield.ai",
            token=self.auth_data.access_token if self.auth_data else None,
        )

    async def sign_in(self, request: ExternalSignInRequest) -> ExternalSignInResponse:
        response = await self.clerk_api.request(
            "POST",
            "/v1/client/sign_ins",
            params={"__clerk_api_version": "2025-04-10", "_clerk_js_version": "5.68.0"},
            data=quote_plus("&".join(f"{k}={v}" for k, v in request.model_dump())),
        )
        return self._validate_response(
            response.data | {"client_cookie": response.cookies.get("__client")}, ExternalSignInResponse
        )
        # Cookies: AMP_684fc54ce3

    async def touch_session(self) -> ExternalTouchSessionResponse:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        response = await self.clerk_api.request(
            "POST",
            f"/v1/client/sessions/{self.auth_data.session_id}/touch",
            params={"__clerk_api_version": "2025-04-10", "_clerk_js_version": "5.68.0"},
        )
        return self._validate_response(response.data, ExternalTouchSessionResponse)

    async def get_current_user(self) -> ExternalGetUserResponse:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        response = await self.fnf_api.request("GET", "https://fnf.higgsfield.ai/user")
        return self._validate_response(response.data, ExternalGetUserResponse)

    async def refresh_token(self) -> ExternalToken:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        response = await self.clerk_api.request(
            "POST",
            f"/v1/client/sessions/{self.auth_data.session_id}/tokens",
            params={"__clerk_api_version": "2025-04-10", "_clerk_js_version": "5.68.0"},
        )
        return self._validate_response(response.data, ExternalToken)

    async def get_video_motions(self, request: ExternalGetMotionsRequest) -> ExternalGetMotionsResponse:
        response = await self.fnf_api.request("GET", "/motions", params=request.model_dump(exclude_none=True))
        return self._validate_response(response.data, ExternalGetMotionsResponse)

    async def create_media_upload_link(self) -> ExternalCreateMediaLinkResponse:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        response = await self.fnf_api.request("POST", "/media")
        return self._validate_response(response.data, ExternalCreateMediaLinkResponse)

    async def upload_media(self, media_link: ExternalCreateMediaLinkResponse, media: BytesIO) -> None:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        await self.http_client.put(
            media_link.upload_url,
            headers={"Content-Type": "image/jpeg"},
            data=media.read()
        )
        with suppress(IntegrationInvalidResponseException):  # Endpoint returns null
            await self.fnf_api.request("POST", f"/media/{media_link.id}/upload")
        logger.debug(f"Uploaded media {media_link.id}")
        # PUT {media_link.upload_url}
        # Headers: Host: fast-and-furious-input-prod-20250325165756276100000002.s3.amazonaws.com
        # POST https://fnf.higgsfield.ai/media/{media_link.id}/upload
        # Headers: Authorization
        ...

    async def start_image2video_generation(
        self, request: ExternalImage2VideoGenerationRequest
    ) -> ExternalImage2VideoGenerationResponse:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        logger.debug(f"Sending image2video request: {request}")
        try:
            response = await self.fnf_api.request("POST", "/jobs/image2video", json=request.model_dump(mode="json"))
        except IntegrationRequestException as e:
            if "not_enough_credits" in str(e):
                logger.bind(name="balance").error(f"Unsufficient https://higgsfield.ai credits ({str(e)}) in session {self.auth_data.session_id}")
            if e.message is not None and "Internal Server Error" in str(e):
                raise IntegrationRequestException(
                    message="Higgsfield internal error. Probably content moderation not passed"
                ) from e
            raise e from e
        return self._validate_response(response.data, ExternalImage2VideoGenerationResponse)

    async def get_job_set(self, job_set_id: str) -> ExternalJobSet:
        if self.auth_data is None:
            raise ValueError("Failed to send external request: Attempt to request without credentials")
        response = await self.fnf_api.request("GET", f"/job-sets/{job_set_id}")
        return self._validate_response(response.data, ExternalJobSet)
        # GET https://fnf.higgsfield.ai/job-sets/{job_set_id}
        # Headers: Authorization
        ...
