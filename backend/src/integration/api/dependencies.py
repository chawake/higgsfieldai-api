from src.integration.application.auth_client import ExternalAuthClient
from src.account.application.interfaces.auth_client import IAuthClient


def get_auth_client() -> IAuthClient:
    return ExternalAuthClient()
