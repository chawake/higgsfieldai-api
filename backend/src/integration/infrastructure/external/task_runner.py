from uuid import UUID

from src.account.domain.dtos import AccountTokenDTO
from src.integration.domain.mappers import AccountTokenDTOToExternalAuthDataMapper
from src.integration.domain.entities import IntegrationTask
from src.task.application.interfaces.task_runner import ITaskRunner
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.schemas import (
    ExternalImage2VideoGenerationRequest,
)
from src.integration.application.interfaces.generation_repository import IGenerationRepository


class ExternalTaskRunner(ITaskRunner[IntegrationTask, ExternalImage2VideoGenerationRequest]):
    def __init__(self, client: ExternalClient, generation_repository: IGenerationRepository) -> None:
        self.client = client
        self.generation_repository = generation_repository

    async def start(
        self, task_id: UUID, token: AccountTokenDTO, data: ExternalImage2VideoGenerationRequest
    ) -> IntegrationTask:
        auth_data = AccountTokenDTOToExternalAuthDataMapper().map_one(token)

        response = await self.client.start_image2video_generation(auth_data, data)
        await self.generation_repository.create(task_id=task_id, external_id=response.job_sets[0].id)

        return IntegrationTask(
            status=response.job_sets[0].jobs[0].status,
            result=response.job_sets[0].jobs[0].result.url if response.job_sets[0].jobs[0].result else None,
        )

    async def get_result(self, task_id: UUID, token: AccountTokenDTO) -> IntegrationTask | None:
        generation = await self.generation_repository.get_by_task_id(task_id)
        auth_data = AccountTokenDTOToExternalAuthDataMapper().map_one(token)

        response = await self.client.get_job_set(auth_data, generation.external_id)

        return IntegrationTask(
            status=response.jobs[0].status, result=response.jobs[0].result.url if response.jobs[0].result else None
        )
