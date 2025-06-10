from pydantic import BaseModel

from src.integration.domain.entities import IntegrationModel


class IntegrationTaskRunParamsDTO(BaseModel):
    prompt: str
    motion_id: str | None = None
    model: IntegrationModel = IntegrationModel.lite
