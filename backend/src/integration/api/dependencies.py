from fastapi import Depends
from src.account.domain.dtos import AccountTokenDTO
from src.integration.application.auth_client import ExternalAuthClient
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.task_runner import ExternalTaskRunner
from src.integration.infrastructure.generation_repository import InMemoryGenerationRepository
from src.integration.application.interfaces.generation_repository import IGenerationRepository

from src.account.api.dependencies import get_available_account_token
from src.account.application.interfaces.auth_client import IAuthClient
from src.task.application.interfaces.task_runner import ITaskRunner


def get_external_client(account_token: AccountTokenDTO = Depends(get_available_account_token)) -> ExternalClient:
    return ExternalClient(account_token)


def get_generation_repository() -> IGenerationRepository:
    return InMemoryGenerationRepository()


def get_higgsfieldai_task_runner(
    external_client: ExternalClient = Depends(get_external_client),
    generation_repository: IGenerationRepository = Depends(get_generation_repository),
) -> ITaskRunner:
    return ExternalTaskRunner(external_client, generation_repository)


def get_auth_client() -> IAuthClient:
    return ExternalAuthClient()
