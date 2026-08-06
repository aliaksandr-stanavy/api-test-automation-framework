"""Get meme by id endpoint client."""

import allure
import requests
from .endpoint import Endpoint
from .constants import MEME_PATH


class GetMemeById(Endpoint):
    """Client for GET /meme/<id>."""

    @allure.step("Get meme by ID")
    def get_meme_by_id(self, meme_id: int | str | float) -> requests.Response:
        """Fetch a single meme by id.

        Args:
            meme_id: Meme identifier.

        Returns:
            Response object from the get request.
        """
        return self._make_request("GET", f"{MEME_PATH}/{meme_id}")
