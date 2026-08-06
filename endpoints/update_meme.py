"""Update meme endpoint client."""

from typing import Any

import allure
import requests
from utils.types import MemeUpdatePayload

from .endpoint import Endpoint
from .constants import MEME_PATH


class UpdateMeme(Endpoint):
    """Client for PUT /meme/<id>."""

    @allure.step("Update meme")
    def update_meme(
        self,
        meme_id: int | str | float,
        payload: MemeUpdatePayload | dict[str, Any] | None = None,
        raw_body: str | None = None,
    ) -> requests.Response:
        """Update a meme via PUT /meme/<id>.

        Args:
            meme_id: Meme identifier in the path.
            payload: JSON body for the request.
            raw_body: Raw string body (non-JSON); takes precedence when set.

        Returns:
            Response object from the update request.
        """
        return self._request_json_or_raw(
            "PUT",
            f"{MEME_PATH}/{meme_id}",
            payload=payload,
            raw_body=raw_body,
        )
