"""Authorize endpoint client."""

from typing import Any

import allure
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, \
    retry_if_exception_type
from .endpoint import Endpoint
from .constants import AUTHORIZE_PATH, STATUS_OK


class Authorize(Endpoint):
    """Client for /authorize endpoints."""

    @allure.step("Authorize user (POST /authorize)")
    def authorize(self, name: Any) -> requests.Response:
        """Authorize user and obtain a token.

        Args:
            name: Username for POST /authorize.

        Returns:
            Response object from the authorize request.
        """
        return self.authorize_with_payload({"name": name})

    @allure.step("Authorize with custom JSON body")
    def authorize_with_payload(self, payload: Any) -> requests.Response:
        """Send POST /authorize with an arbitrary JSON body.

        Args:
            payload: JSON-serializable request body.

        Returns:
            Response object from the authorize request.
        """
        return self._make_request(
            "POST",
            AUTHORIZE_PATH,
            json=payload
        )

    @allure.step("Get token status (GET /authorize/{token})")
    def get_token_status(self, token: str) -> requests.Response:
        """Check whether a token is still alive.

        Args:
            token: Token string to validate.

        Returns:
            Response object from the status request.
        """
        return self._make_request(
            "GET",
            f"{AUTHORIZE_PATH}/{token}"
        )

    @allure.step("Delete token")
    def delete_token(self, token: str) -> requests.Response:
        """Invalidate a token via kill endpoint.

        Args:
            token: Token string to delete.

        Returns:
            Response object from the kill request.
        """
        self.set_token(None)
        return self._make_request(
            "GET",
            f"{AUTHORIZE_PATH}/kill/{token}"
        )

    @allure.step("Wait until token is deleted (polling)")
    def wait_until_deleted(
        self, token: str, attempts: int = 10, delay: int = 2
    ) -> None:
        """Poll until the token returns 404 or attempts are exhausted.

        Args:
            token: Token string to poll.
            attempts: Max polling attempts.
            delay: Seconds between attempts.

        Raises:
            AssertionError: If the token is still active (or any status
                other than 200/404) after all polling attempts.
        """
        @retry(
            stop=stop_after_attempt(attempts),
            wait=wait_fixed(delay),
            retry=retry_if_exception_type(AssertionError),
            reraise=True
        )
        def _check() -> None:
            with allure.step(f"Is token {token} deleted?"):
                self.get_token_status(token)
                assert self.response is not None, (
                    "Response must be set after get_token_status"
                )
                if self.response.status_code == STATUS_OK:
                    raise AssertionError(f"Token {token} is still active")
                self.check_status_is_404()

        _check()
