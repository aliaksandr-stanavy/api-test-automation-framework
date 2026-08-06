"""Negative test case builders for Memes API."""

import copy
from typing import Any

from endpoints.constants import STATUS_BAD_REQUEST, STATUS_NOT_FOUND

from .common_data import (
    get_type_validation_cases,
    get_missing_field_cases,
    get_put_id_type_validation_cases,
    get_case,
)


def _case(
    description: str,
    payload: Any = None,
    *,
    raw_body: str | None = None,
    inject_id: bool = True,
    expected_status: int = STATUS_BAD_REQUEST,
) -> dict[str, Any]:
    """Build a unified negative case for POST/PUT.

    Args:
        description: Human-readable case id for pytest/Allure.
        payload: JSON body, or None when only raw_body is used.
        raw_body: Raw non-JSON body string.
        inject_id: If True, the test injects a real meme id into payload.
        expected_status: Expected HTTP status code.

    Returns:
        Negative case dict.
    """
    return {
        "description": description,
        "payload": copy.deepcopy(payload) if payload is not None else None,
        "raw_body": raw_body,
        "inject_id": inject_id,
        "expected_status": expected_status,
    }


def get_negative_test_cases_post() -> list[dict[str, Any]]:
    """Negative POST cases: types, missing fields, empty/non-JSON body.

    Returns:
        List of negative case dicts.
    """
    cases = [
        _case(desc, payload, inject_id=False)
        for desc, payload in get_type_validation_cases()
    ]
    cases.extend(
        _case(desc, payload, inject_id=False)
        for desc, payload in get_missing_field_cases()
    )
    cases.extend([
        _case("Empty JSON object", {}, inject_id=False),
        _case("Empty JSON array", [], inject_id=False),
        _case("Null JSON body", None, inject_id=False),
        _case(
            "Non-JSON raw body",
            raw_body="this is not json",
            inject_id=False,
        ),
    ])
    return cases


def get_negative_test_cases_put() -> list[dict[str, Any]]:
    """Negative PUT cases expected to fail with 400.

    inject_id=True means the test sets a real meme_id on the payload.
    inject_id=False is used for invalid/missing id or raw body cases.

    Returns:
        List of negative case dicts.
    """
    cases = [
        _case(desc, payload, inject_id=True)
        for desc, payload in get_type_validation_cases()
    ]
    cases.extend(
        _case(desc, payload, inject_id=True)
        for desc, payload in get_missing_field_cases()
    )
    cases.extend(
        _case(desc, payload, inject_id=False)
        for desc, payload in get_put_id_type_validation_cases()
    )
    cases.append(_case("Missing field: id", get_case(), inject_id=False))
    cases.extend([
        _case("Empty JSON object", {}, inject_id=False),
        _case(
            "Non-JSON raw body",
            raw_body="this is not json",
            inject_id=False,
        ),
    ])
    return cases


def _invalid_resource_ids() -> list[tuple[str, int | str]]:
    """Shared invalid id samples for GET/DELETE.

    Returns:
        List of (description, id_value) tuples.
    """
    return [
        ("Non-existent ID", 99999),
        ("Negative ID", -1),
        ("Zero ID", 0),
        ("String ID", "invalid"),
    ]


def get_negative_test_cases_get() -> list[dict[str, Any]]:
    """Negative GET-by-id cases.

    Returns:
        List of dicts with description, id, expected_status.
    """
    return [
        {
            "description": f"GET with {desc}",
            "id": value,
            "expected_status": STATUS_NOT_FOUND,
        }
        for desc, value in _invalid_resource_ids()
    ]


def get_negative_test_cases_delete() -> list[dict[str, Any]]:
    """Negative DELETE-by-id cases.

    Returns:
        List of dicts with description, id, expected_status.
    """
    return [
        {
            "description": f"DELETE with {desc}",
            "id": value,
            "expected_status": STATUS_NOT_FOUND,
        }
        for desc, value in _invalid_resource_ids()
    ]
