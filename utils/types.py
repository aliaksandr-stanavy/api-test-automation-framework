"""TypedDict models for Memes API payloads."""

from typing import Any, NotRequired, TypedDict


class MemePayload(TypedDict):
    """Valid body for POST /meme (BRD required fields)."""

    text: str
    url: str
    tags: list[str]
    info: dict[str, Any]
    extra_field: NotRequired[str]


class MemeUpdatePayload(MemePayload):
    """Valid body for PUT /meme/<id> (BRD requires id: int)."""

    id: int


class PositiveMemeCase(TypedDict):
    """Static positive case shape used in parametrized tests."""

    description: str
    payload: MemePayload
