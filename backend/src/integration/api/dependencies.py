from typing import Annotated

from fastapi import Depends
from src.account.domain.dtos import AccountTokenDTO
from src.integration.application.auth_client import ExternalAuthClient
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.task_runner import ExternalTaskRunner
from src.integration.infrastructure.generation_repository import InMemoryGenerationRepository
from src.integration.application.interfaces.generation_repository import IGenerationRepository

from src.account.application.interfaces.auth_client import IAuthClient
from src.task.application.interfaces.task_runner import ITaskRunner


def get_external_client(account_token: AccountTokenDTO | None = None) -> ExternalClient:
    return ExternalClient(account_token)


def get_generation_repository() -> IGenerationRepository:
    return InMemoryGenerationRepository()


def get_higgsfieldai_task_runner(account_token: AccountTokenDTO | None = None) -> ITaskRunner:
    external_client = get_external_client(account_token)
    generation_repository = get_generation_repository()
    return ExternalTaskRunner(external_client, generation_repository)


def get_auth_client() -> IAuthClient:
    return ExternalAuthClient()


def _rest_get_external_client() -> ExternalClient:
    return ExternalClient(account_token=None)


ExternalClientDepend = Annotated[ExternalClient, Depends(_rest_get_external_client)]
