from src.integration.application.auth_client import ExternalAuthClient
from src.integration.infrastructure.external.client import ExternalClient
from src.integration.infrastructure.external.task_runner import ExternalTaskRunner
from src.integration.infrastructure.generation_repository import InMemoryGenerationRepository
from src.integration.application.interfaces.generation_repository import IGenerationRepository

from src.account.application.interfaces.auth_client import IAuthClient
from src.task.application.interfaces.task_runner import ITaskRunner


def get_external_client() -> ExternalClient:
    return ExternalClient()


def get_generation_repository() -> IGenerationRepository:
    return InMemoryGenerationRepository()


def get_higgsfieldai_task_runner() -> ITaskRunner:
    external_client = get_external_client()
    generation_repository = get_generation_repository()
    return ExternalTaskRunner(external_client, generation_repository)


def get_auth_client() -> IAuthClient:
    return ExternalAuthClient()
