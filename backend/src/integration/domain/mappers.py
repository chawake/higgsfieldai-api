from random import randint
from src.account.domain.dtos import AccountTokenDTO
from src.integration.infrastructure.external.entities import ExternalAuthData, ExternalMedia
from src.integration.infrastructure.external.schemas import ExternalImage2VideoGenerationRequest
from src.task.domain.entities import TaskRun


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


class TaskRunToExternalRequestMapper:
    def map_one(self, task_run: TaskRun, input_image: ExternalMedia) -> ExternalImage2VideoGenerationRequest:
        return ExternalImage2VideoGenerationRequest(
            params=ExternalImage2VideoGenerationRequest.Params(
                enhance_prompt=False,
                prompt=task_run.prompt,
                motion_id=task_run.motion_id or "d2389a9a-91c2-4276-bc9c-c9e35e8fb85a",  # 'General' motion, required by api
                seed=randint(1, 1000000),
                input_image=input_image
            )
        )
