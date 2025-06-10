import abc
from uuid import UUID

from src.integration.domain.entities import IntegrationGeneration


class IGenerationRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, task_id: UUID, external_id: str) -> IntegrationGeneration: ...

    @abc.abstractmethod
    async def get_by_task_id(self, task_id: UUID) -> IntegrationGeneration: ...

    @abc.abstractmethod
    async def delete_by_task_id(self, task_id: UUID) -> None: ...
