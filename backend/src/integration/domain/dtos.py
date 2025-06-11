from typing import Literal
from pydantic import BaseModel

from src.integration.domain.entities import IntegrationModel


class IntegrationTaskRunParamsDTO(BaseModel):
    prompt: str
    motion_id: str | None = None
    model: IntegrationModel = IntegrationModel.lite


class IntegrationHiggsfieldMotionDTO(BaseModel):
    class Media(BaseModel):
        url: str
        type: str

    id: str
    name: str
    priority: int
    media: Media


class IntegrationHiggsfieldMotionRequestDTO(BaseModel):
    size: int = 30
    search: str = ""
    category: (
        Literal["new", "trending", "vfx", "basic_camera_control", "epic_camera_control", "catch_the_pulse", "mix"]
        | None
    ) = None
