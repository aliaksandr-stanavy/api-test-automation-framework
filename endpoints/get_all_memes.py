"""Get all memes endpoint client."""

import allure
import requests
from .endpoint import Endpoint
from .constants import MEME_PATH


class GetAllMemes(Endpoint):
    """Client for GET /meme."""

    @allure.step("Get all memes")
    def get_all_memes(self) -> requests.Response:
        """Fetch the full memes list.

        Returns:
            Response object from the list request.
        """
        return self._make_request("GET", MEME_PATH)
