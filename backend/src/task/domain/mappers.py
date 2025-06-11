from src.task.domain.dtos import TaskResultDTO
from src.task.domain.entities import TaskSource, TaskStatus
from src.task.application.interfaces.task_runner import TResponse

from src.integration.domain.entities import IntegrationTask


class IntegrationResponseToDomainMapper:
    def __init__(self, source: TaskSource | None = None) -> None:
        self.source = source

    def map_one(self, data: TResponse) -> TaskResultDTO:
        self.source = self._define_source(data)

        if self.source == TaskSource.higgsfieldai:
            return HiggsfieldaiResponseToDomainMapper().map_one(data)

        raise ValueError("Failed to map integration response: Unknown data source")

    def _define_source(self, data: TResponse) -> TaskSource | None:
        if self.source:
            return self.source
        if hasattr(data, "status") and hasattr(data, "result"):
            return TaskSource.higgsfieldai


class HiggsfieldaiResponseToDomainMapper:
    def map_one(self, data: IntegrationTask) -> TaskResultDTO:
        return TaskResultDTO(
            status=self._map_status(data.status),
            result=data.result,
            error=None
        )

    @staticmethod
    def _map_status(status: str) -> TaskStatus:
        if status == "queued":
            return TaskStatus.queued
        elif status == "in_progress":
            return TaskStatus.started
        elif status == "completed":
            return TaskStatus.finished
        raise ValueError(f"Failed to map response: Unknown status {status}")
