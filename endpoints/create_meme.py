"""Create meme endpoint client."""

from typing import Any

import allure
import requests
from utils.types import MemePayload

from .endpoint import Endpoint
from .constants import MEME_PATH


class CreateMeme(Endpoint):
    """Client for POST /meme."""

    @allure.step("Create a new meme")
    def create_meme(
        self,
        payload: MemePayload | dict[str, Any] | None = None,
        raw_body: str | None = None,
    ) -> requests.Response:
        """Create a meme via POST /meme.

        Args:
            payload: JSON body for the request.
            raw_body: Raw string body (non-JSON); takes precedence when set.

        Returns:
            Response object from the create request.
        """
        return self._request_json_or_raw(
            "POST", MEME_PATH, payload=payload, raw_body=raw_body
        )
