"""Static positive test cases aligned with BRD."""

from typing import cast

from .common_data import get_case
from .types import MemePayload, PositiveMemeCase


def get_positive_test_cases() -> list[PositiveMemeCase]:
    """Return static positive cases without invented boundaries.

    Critical base/min/max coverage lives in tests via data_generator.

    Returns:
        List of dicts with description and payload.
    """
    return [
        {
            "description": "Empty tags",
            "payload": cast(MemePayload, get_case({"tags": []})),
        },
        {
            "description": "Empty info",
            "payload": cast(MemePayload, get_case({"info": {}})),
        },
        {
            "description": "Subdomain URL",
            "payload": cast(
                MemePayload,
                get_case({"url": "https://sub.example.com/x.jpg"}),
            ),
        },
        {
            "description": "Extra field tolerated",
            "payload": cast(
                MemePayload,
                get_case({"extra_field": "ok"}),
            ),
        },
    ]
