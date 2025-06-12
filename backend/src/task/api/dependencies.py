from typing import Annotated

from fastapi import Depends

from src.account.application.use_cases.refresh_account_tokens import RefreshAccountTokensUseCase
from src.account.domain.dtos import AccountTokenDTO
from src.account.api.dependencies import get_account_token_refresher, get_available_account_token
from src.integration.api.dependencies import get_higgsfieldai_task_runner
from src.task.application.interfaces.http_client import IHttpClient
from src.task.infrastructure.db.unit_of_work import TaskUnitOfWork
from src.task.application.interfaces.task_uow import ITaskUnitOfWork
from src.task.application.interfaces.task_runner import ITaskRunner
from src.task.infrastructure.http.client import AsyncHttpClient


def get_task_uow() -> ITaskUnitOfWork:
    return TaskUnitOfWork()


def get_task_runner(account_token: AccountTokenDTO = Depends(get_available_account_token)) -> ITaskRunner:
    return get_higgsfieldai_task_runner(account_token)


def get_http_client() -> IHttpClient:
    return AsyncHttpClient()


TaskUoWDepend = Annotated[ITaskUnitOfWork, Depends(get_task_uow)]
TaskRunnerDepend = Annotated[ITaskRunner, Depends(get_task_runner)]
AccountTokenDepend = Annotated[AccountTokenDTO, Depends(get_available_account_token)]
AccountTokenRefreshedDepend = Annotated[RefreshAccountTokensUseCase, Depends(get_account_token_refresher)]
HttpClientDepend = Annotated[IHttpClient, Depends(get_http_client)]
