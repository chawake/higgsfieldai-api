"""Higgsfield API request/response schemas"""

from typing import Literal

from pydantic import Field, BaseModel

from src.integration.infrastructure.external.entities import (
    ExternalMedia,
    ExternalClient,
    ExternalJobSet,
    ExternalSession,
    ExternalSignInAttempt,
    ExternalVideoMotionControl,
)


class ExternalSignInRequest(BaseModel):
    identifier: str
    password: str


class ExternalSignInResponse(BaseModel):
    response: ExternalSignInAttempt
    client: ExternalClient

    client_cookie: str | None = None


class ExternalTouchSessionResponse(BaseModel):
    response: ExternalSession
    client: ExternalClient


class ExternalGetUserResponse(BaseModel):
    id: str
    subscription_credits: float
    total_plan_credits: int
    plan_ends_at: str


class ExternalGetMotionsRequest(BaseModel):
    size: int
    search: str = ""
    category: (
        Literal["new", "trending", "vfx", "basic_camera_control", "epic_camera_control", "catch_the_pulse", "mix"]
        | None
    ) = None


class ExternalGetMotionsResponse(BaseModel):
    items: list[ExternalVideoMotionControl]
    total: int


class ExternalCreateMediaLinkResponse(BaseModel):
    id: str
    url: str
    upload_url: str
    content_type: str


class ExternalImage2VideoGenerationRequest(BaseModel):
    class Params(BaseModel):
        enhance_prompt: bool
        frames: int = 81
        height: int = 1536
        width: int = 1024
        input_audio: None = None
        input_image: ExternalMedia
        model: Literal["lite", "standard", "turbo"] = "lite"
        motion_id: str | None = None
        prompt: str
        seed: int = Field(description="Random generated", gt=0)
        steps: int = 30

    params: Params


class ExternalImage2VideoGenerationResponse(BaseModel):
    id: str
    job_sets: list[ExternalJobSet]
