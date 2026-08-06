"""Shared meme payload builders for positive and negative cases."""

import copy
from typing import Any

from .types import MemePayload


def get_base_meme() -> MemePayload:
    """Return a fresh base meme payload.

    Returns:
        Dict with text, url, tags, and info fields.
    """
    return {
        "text": "Valid text",
        "url": "https://example.com/image.jpg",
        "tags": ["tag1", "tag2"],
        "info": {"key": ["value1", "value2"]},
    }


def get_case(
    overrides: dict[str, Any] | None = None,
    remove_field: str | None = None,
) -> dict[str, Any]:
    """Return an independent copy of the base meme payload.

    Used for both valid overrides and intentional invalid negative bodies.
    Return type is a plain dict because negatives break TypedDict contracts.

    Args:
        overrides: Optional field overrides to merge into the base payload.
        remove_field: Optional field name to delete from the payload.

    Returns:
        Deep-copied meme payload dict.
    """
    case = copy.deepcopy(dict(get_base_meme()))
    if overrides:
        case.update(copy.deepcopy(overrides))
    if remove_field:
        del case[remove_field]
    return case


def get_missing_field_cases() -> list[tuple[str, dict[str, Any]]]:
    """Build cases with one required field removed.

    Returns:
        List of (description, payload) tuples.
    """
    return [
        (f"Missing field: {field}", get_case(remove_field=field))
        for field in ["text", "url", "tags", "info"]
    ]


def get_type_validation_cases() -> list[tuple[str, dict[str, Any]]]:
    """Build cases with invalid field types per BRD.

    Returns:
        List of (description, payload) tuples.
    """
    return [
        ("Text as int", get_case({"text": 12345})),
        ("Url as int", get_case({"url": 12345})),
        ("Tags as string", get_case({"tags": "not_array"})),
        ("Tags as int", get_case({"tags": 123})),
        ("Tags as object", get_case({"tags": {"a": 1}})),
        ("Info as None", get_case({"info": None})),
        ("Info as array", get_case({"info": ["not", "object"]})),
        ("Info as string", get_case({"info": "not_object"})),
    ]


def get_put_id_type_validation_cases() -> list[tuple[str, dict[str, Any]]]:
    """Build PUT cases with invalid body id types.

    Returns:
        List of (description, payload) tuples.
    """
    return [
        ("Id as string", get_case({"id": "not-an-int"})),
        ("Id as float", get_case({"id": 1.5})),
        ("Id as null", get_case({"id": None})),
    ]
