from uuid import UUID

from src.db.exceptions import DBModelNotFoundException
from src.integration.domain.entities import IntegrationGeneration
from src.integration.application.interfaces.generation_repository import IGenerationRepository

generations = []


class InMemoryGenerationRepository(IGenerationRepository):
    def __init__(self) -> None:
        global generations
        self.generations = generations

    async def create(self, task_id: UUID, external_id: str) -> IntegrationGeneration:
        model = IntegrationGeneration(task_id=task_id, external_id=external_id)
        self.generations.append(model)
        return model

    async def get_by_task_id(self, task_id: UUID) -> IntegrationGeneration:
        for gen in self.generations:
            if gen.task_id == task_id:
                return gen
        raise DBModelNotFoundException()

    async def delete_by_task_id(self, task_id: UUID) -> None:
        for gen in self.generations:
            if gen.task_id == task_id:
                self.generations.remove(gen)
                return
        raise DBModelNotFoundException()
