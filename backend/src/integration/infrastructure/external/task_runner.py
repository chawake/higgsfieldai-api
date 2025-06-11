from io import BytesIO
from uuid import UUID

from src.task.domain.entities import TaskRun
from src.integration.domain.mappers import TaskRunToExternalRequestMapper
from src.integration.domain.entities import IntegrationTask
from src.task.application.interfaces.task_runner import ITaskRunner
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.schemas import (
    ExternalImage2VideoGenerationRequest,
)
from src.integration.infrastructure.external.entities import ExternalMedia
from src.integration.application.interfaces.generation_repository import IGenerationRepository


class ExternalTaskRunner(ITaskRunner[IntegrationTask, ExternalImage2VideoGenerationRequest]):
    def __init__(self, client: ExternalClient, generation_repository: IGenerationRepository) -> None:
        self.client = client
        self.generation_repository = generation_repository

    async def start(self, task_id: UUID, data: TaskRun) -> IntegrationTask:
        if data.image is None:
            return await self._start_text2video(task_id, data)
        return await self._start_image2video(task_id, data)

    async def _start_text2video(self, task_id: UUID, data: TaskRun) -> IntegrationTask:
        raise NotImplementedError()

    async def _start_image2video(self, task_id: UUID, data: TaskRun) -> IntegrationTask:
        media = await self.upload_image(data.image)
        request = TaskRunToExternalRequestMapper().map_one(data, media)
        response = await self.client.start_image2video_generation(request)
        await self.generation_repository.create(task_id=task_id, external_id=response.job_sets[0].id)

        return IntegrationTask(
            status=response.job_sets[0].jobs[0].status,
            result=response.job_sets[0].jobs[0].result.url if response.job_sets[0].jobs[0].result else None,
        )

    async def get_result(self, task_id: UUID) -> IntegrationTask | None:
        generation = await self.generation_repository.get_by_task_id(task_id)
        response = await self.client.get_job_set(generation.external_id)

        return IntegrationTask(
            status=response.jobs[0].status, result=response.jobs[0].result.url if response.jobs[0].result else None
        )

    async def upload_image(self, image: BytesIO) -> ExternalMedia:
        media_link = await self.client.create_media_upload_link()
        await self.client.upload_media(media_link, image)
        return ExternalMedia(id=media_link.id, url=media_link.url)
