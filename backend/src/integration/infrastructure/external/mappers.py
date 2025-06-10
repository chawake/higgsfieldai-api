import random
from typing import Literal

from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskRun, TaskStatus
from src.integration.infrastructure.external.schemas import (
    ExternalImage2VideoGenerationRequest,
    ExternalImage2VideoGenerationResponse,
)


class TaskRunToRequestMapper:
    def map_one(self, data: TaskRun) -> ExternalImage2VideoGenerationRequest:
        return ExternalImage2VideoGenerationRequest(
            params=ExternalImage2VideoGenerationRequest.Params(enhance_prompt=False, seed=random.randint(1, 1000000))
        )


class ResponseToTaskResultDTOMapper:
    def map_one(self, data: ExternalImage2VideoGenerationResponse) -> TaskResultDTO:
        return TaskResultDTO(
            status=self._map_status(data.job_sets[0].jobs[0].status),
            result=data.job_sets[0].jobs[0].result.url,
            error=None,
        )

    @staticmethod
    def _map_status(status: Literal["queued", "in_progress", "completed"]) -> TaskStatus:
        if status == "queued":
            return TaskStatus.queued
        elif status == "in_progress":
            return TaskStatus.started
        elif status == "completed":
            return TaskStatus.finished
        raise ValueError(f"Cannot map response: Unknown response status {status}")
