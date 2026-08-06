"""Delete meme endpoint client."""

import allure
import requests
from .endpoint import Endpoint
from .constants import MEME_PATH


class DeleteMeme(Endpoint):
    """Client for DELETE /meme/<id>."""

    @allure.step("Delete meme")
    def delete_meme(self, meme_id: int | str | float) -> requests.Response:
        """Delete a meme by id.

        Args:
            meme_id: Meme identifier.

        Returns:
            Response object from the delete request.
        """
        return self._make_request("DELETE", f"{MEME_PATH}/{meme_id}")
