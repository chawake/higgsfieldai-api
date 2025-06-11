import asyncio
from io import BytesIO
from uuid import UUID

from loguru import logger

from src.task.domain.dtos import TaskCreateDTO, TaskResultDTO
from src.account.domain.dtos import AccountTokenDTO
from src.task.domain.mappers import IntegrationResponseToDomainMapper
from src.task.domain.entities import TaskRun, TaskStatus, TaskUpdate
from src.integration.domain.exceptions import IntegrationRequestException
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.application.interfaces.task_runner import TResponse, ITaskRunner


class RunTaskUseCase:
    TIMEOUT_SECONDS = 5 * 60

    def __init__(self, uow: ITaskUnitOfWork, runner: ITaskRunner, token: AccountTokenDTO) -> None:
        self.uow = uow
        self.runner = runner
        self.token = token

    async def execute(self, task_id: UUID, dto: TaskCreateDTO, image: BytesIO | None) -> None:
        """Run it in background"""
        command = TaskRun(**dto.model_dump(), image=image)
        logger.info(f"Running task {task_id}")
        logger.debug(f"Task {task_id} params: {command}")
        _, error = await self._run(task_id, command)

        if error is not None:
            await self._set_task_status(task_id, status=TaskStatus.failed, error=error)
            return

        result, error = await self._wait_for_result(task_id)
        if error is not None:
            await self._set_task_status(task_id, status=TaskStatus.failed, error=error)
            return

        logger.info(f"Task {task_id} result: {result}")
        await self._store_result(task_id, result)

    async def _store_result(self, task_id: UUID, result: TaskResultDTO):
        async with self.uow:
            await self.uow.tasks.update_by_pk(
                task_id, TaskUpdate(status=result.status, error=result.error, result=result.result)
            )
            await self.uow.commit()

    async def _set_task_status(self, task_id: UUID, status: TaskStatus, error: str | None = None):
        async with self.uow:
            await self.uow.tasks.update_by_pk(task_id, TaskUpdate(status=status, error=error))
            await self.uow.commit()

    async def _wait_for_result(self, task_id: UUID) -> tuple[TaskResultDTO | None, None | str]:
        for _ in range(self.TIMEOUT_SECONDS):
            await asyncio.sleep(1)

            result = await self.runner.get_result(task_id)
            result_domain = IntegrationResponseToDomainMapper().map_one(result)
            if result_domain.status is TaskStatus.finished:
                return result_domain, None
        return None, "Timeout"

    async def _run(self, task_id: UUID, command: TaskRun) -> tuple[TResponse | None, None | str]:
        try:
            result = await asyncio.wait_for(
                self.runner.start(task_id, command), timeout=self.TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            return None, "Generation run error: Timeout"
        except IntegrationRequestException as e:
            logger.opt(exception=True).warning(e)
            return None, "Request error: " + str(e)
        except Exception as e:
            logger.exception(e)
            return None, "Internal exception: " + str(e)
        return result, None
