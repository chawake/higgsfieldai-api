"""Higgsfield API entities"""

from typing import Literal

from pydantic import BaseModel


class ExternalUser(BaseModel):
    id: str
    first_name: str
    last_name: str


class ExternalToken(BaseModel):
    jwt: str


class ExternalSession(BaseModel):
    id: str
    status: str
    last_active_token: ExternalToken


class ExternalClient(BaseModel):
    id: str
    last_active_session_id: str
    sessions: list[ExternalSession]


class ExternalSignInAttempt(BaseModel):
    id: str
    status: str
    identifier: str
    created_session_id: str


class ExternalAuthData(BaseModel):
    client_cookie: str
    session_id: str
    access_token: str


class ExternalVideoMotionControl(BaseModel):
    class Media(BaseModel):
        url: str
        type: str

    id: str
    name: str
    priority: int
    media: Media


class ExternalMedia(BaseModel):
    id: str
    type: str = "media_input"
    url: str  # From ExternalCreateMediaLinkResponse.url


class ExternalJob(BaseModel):
    class Result(BaseModel):
        type: str
        url: str

    id: str
    status: Literal["queued", "in_progress", "completed"]
    result: Result | None = None
    board_ids: list


class ExternalJobSet(BaseModel):
    id: str
    type: str = "image2video"
    project_id: str
    jobs: list[ExternalJob]
