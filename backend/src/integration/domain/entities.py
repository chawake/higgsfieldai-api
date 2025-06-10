from io import BytesIO
from enum import Enum
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict


class IntegrationModel(str, Enum):
    lite = "lite"
    standard = "standard"
    turbo = "turbo"


class IntegrationTask(BaseModel):
    status: Literal["queued", "in_progress", "completed"]
    result: str | None = None


class IntegrationTaskStart(BaseModel):
    prompt: str
    motion_id: str | None = None
    model: IntegrationModel = IntegrationModel.lite
    image: BytesIO | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class IntegrationGeneration(BaseModel):
    task_id: UUID
    external_id: str
