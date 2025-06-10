import abc
from uuid import UUID
from typing import Generic, TypeVar

from src.account.domain.dtos import AccountTokenDTO

TResponse = TypeVar("TResponse")
TRequest = TypeVar("TRequest")


class ITaskRunner(abc.ABC, Generic[TResponse, TRequest]):
    @abc.abstractmethod
    async def start(self, task_id: UUID, token: AccountTokenDTO, data: TRequest) -> TResponse: ...

    @abc.abstractmethod
    async def get_result(self, task_id: UUID, token: AccountTokenDTO) -> TResponse | None: ...
