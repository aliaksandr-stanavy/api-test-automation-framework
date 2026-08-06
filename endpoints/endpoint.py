"""Base HTTP endpoint client and shared response assertions."""

import json
from typing import Any

import requests
import allure
import pytest
from .constants import (
    BASE_URL,
    STATUS_OK,
    STATUS_UNAUTHORIZED,
    STATUS_FORBIDDEN,
    STATUS_NOT_FOUND,
    CONTENT_TYPE_JSON,
    AUTHORIZATION_HEADER,
)

REQUIRED_MEME_FIELDS = ("id", "text", "url", "tags", "info")


class Endpoint:
    """Shared API client helpers for Memes API endpoints."""

    def __init__(self) -> None:
        """Initialize base URL, empty response state, and JSON headers."""
        self.url = BASE_URL
        assert self.url, "BASE_URL is not set (check .env)"
        self.response: requests.Response | None = None
        self.json: Any | None = None
        self.headers: dict[str, str] = {"Content-Type": CONTENT_TYPE_JSON}

    def set_token(self, token):
        """Set or clear the Authorization header.

        Args:
            token: Auth token string, or None/empty to remove the header.
        """
        if token:
            self.headers[AUTHORIZATION_HEADER] = token
        elif AUTHORIZATION_HEADER in self.headers:
            del self.headers[AUTHORIZATION_HEADER]

    def _headers_for_allure(self):
        """Return headers copy with Authorization token masked."""
        headers = dict(self.headers)
        if AUTHORIZATION_HEADER in headers and headers[AUTHORIZATION_HEADER]:
            headers[AUTHORIZATION_HEADER] = "***"
        return headers

    def _body_for_allure(self, kwargs):
        """Extract request body from requests.kwargs for Allure."""
        if "json" in kwargs:
            return kwargs["json"]
        if "data" in kwargs:
            return kwargs["data"]
        return None

    def _attach_json_or_text(self, name, payload):
        """Attach payload to Allure as JSON when possible, else as text."""
        if payload is None:
            allure.attach("null", name=name, attachment_type=allure.attachment_type.TEXT)
            return
        if isinstance(payload, (dict, list)):
            allure.attach(
                json.dumps(payload, ensure_ascii=False, indent=2),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )
            return
        allure.attach(
            str(payload),
            name=name,
            attachment_type=allure.attachment_type.TEXT,
        )

    def _attach_request(self, method, full_url, kwargs):
        """Attach HTTP request details to the current Allure step."""
        request_meta = {
            "method": method,
            "url": full_url,
            "headers": self._headers_for_allure(),
        }
        allure.attach(
            json.dumps(request_meta, ensure_ascii=False, indent=2),
            name="request",
            attachment_type=allure.attachment_type.JSON,
        )
        body = self._body_for_allure(kwargs)
        if body is not None:
            self._attach_json_or_text("request_body", body)

    def _attach_response(self):
        """Attach HTTP response status and body to the current Allure step."""
        if self.response is None:
            return
        response_meta = {
            "status_code": self.response.status_code,
            "headers": dict(self.response.headers),
        }
        allure.attach(
            json.dumps(response_meta, ensure_ascii=False, indent=2),
            name="response",
            attachment_type=allure.attachment_type.JSON,
        )
        if self.json is not None:
            self._attach_json_or_text("response_body", self.json)
        else:
            body = self.response.text if self.response.text else ""
            allure.attach(
                body,
                name="response_body",
                attachment_type=allure.attachment_type.TEXT,
            )

    def _make_request(
        self, method: str, path: str, **kwargs: Any
    ) -> requests.Response:
        """Send an HTTP request and parse JSON when possible.

        Attaches request/response details to Allure for debugging.

        Args:
            method: HTTP method name.
            path: URL path appended to BASE_URL.
            **kwargs: Extra arguments passed to requests.request.

        Returns:
            Response object from requests.
        """
        full_url = f"{self.url}{path}"
        self._attach_request(method, full_url, kwargs)
        try:
            self.response = requests.request(
                method,
                full_url,
                headers=self.headers,
                timeout=10,
                **kwargs
            )
            self._parse_response_json()
            self._attach_response()
            return self.response
        except requests.exceptions.RequestException as e:
            allure.attach(
                str(e),
                name="network_error",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(f"Network error on {method} {path}: {e}")
            raise  # unreachable; keeps mypy happy (pytest.fail is NoReturn)

    def _request_json_or_raw(
        self,
        method: str,
        path: str,
        payload: Any = None,
        raw_body: str | None = None,
    ) -> requests.Response:
        """Send JSON payload or raw body via _make_request.

        Args:
            method: HTTP method name.
            path: URL path appended to BASE_URL.
            payload: JSON-serializable body (used when raw_body is None).
            raw_body: Raw string body; takes precedence when set.

        Returns:
            Response object from requests.
        """
        if raw_body is not None:
            return self._make_request(method, path, data=raw_body)
        return self._make_request(method, path, json=payload)

    def _parse_response_json(self) -> None:
        """Parse response body as JSON into self.json, or set None."""
        try:
            assert self.response is not None, (
                "Response must be set before parsing JSON"
            )
            self.json = self.response.json()
        except (ValueError, AttributeError):
            self.json = None

    def _response_body_snippet(self):
        """Return response text for assertion messages, or 'no body'."""
        if (
            self.response is not None
            and hasattr(self.response, "text")
            and self.response.text
        ):
            return self.response.text
        return "no body"

    def _check_status_code(self, expected_code):
        """Assert response status equals expected_code."""
        assert self.response is not None, "Response is None"
        actual_code = self.response.status_code
        body = self._response_body_snippet()

        assert actual_code == expected_code, (
            f"Expected code {expected_code}, got {actual_code}\n"
            f"Response body: {body}"
        )

    @allure.step("Assert status code is 200")
    def check_status_is_200(self):
        """Assert response status code is 200 OK."""
        self._check_status_code(STATUS_OK)

    @allure.step("Assert status code is 404")
    def check_status_is_404(self):
        """Assert response status code is 404 Not Found."""
        self._check_status_code(STATUS_NOT_FOUND)

    @allure.step("Assert status code is 401")
    def check_status_is_401(self):
        """Assert response status code is 401 Unauthorized.

        Used when Authorization is missing, invalid, or the token was killed.
        """
        self._check_status_code(STATUS_UNAUTHORIZED)

    @allure.step("Assert status code is 403")
    def check_status_is_403(self):
        """Assert response status code is 403 Forbidden.

        Used when the caller is authenticated but not the meme owner.
        """
        self._check_status_code(STATUS_FORBIDDEN)

    @allure.step("Assert custom status code")
    def check_status_code(self, code):
        """Assert response status equals the given code.

        Args:
            code: Expected HTTP status code.
        """
        self._check_status_code(code)

    @allure.step("Assert response is JSON")
    def check_response_is_json(self):
        """Assert response body was parsed as JSON."""
        assert self.json is not None, "Response is not JSON or not parsed"

    @allure.step("Assert successful meme response")
    def check_successful_meme_response(self, expected_data: Any) -> None:
        """Assert 200 JSON response and matching meme fields.

        Args:
            expected_data: Dict of expected text/url/tags/info values.

        Raises:
            AssertionError: If status, JSON, or field values do not match.
        """
        self.check_status_is_200()
        self.check_response_is_json()
        body = self.json
        assert body is not None, "Response JSON body is None after parse"

        for key in ["text", "url", "tags", "info"]:
            if key in expected_data:
                actual_val = body.get(key)
                expected_val = expected_data[key]
                assert actual_val == expected_val, (
                    f"Field '{key}' mismatch. "
                    f"Expected: {expected_val}, "
                    f"got: {actual_val}"
                )

    def _extract_memes_list(self):
        """Return the memes list from the last JSON response.

        Returns:
            List of meme dicts.
        """
        self.check_response_is_json()
        memes = (
            self.json.get("data") if isinstance(self.json, dict) else self.json
        )
        memes = memes or []
        assert isinstance(memes, list), (
            "Expected a list of memes (key 'data' or JSON root)"
        )
        return memes

    def _extract_meme_ids(self):
        """Return meme ids from the last list response."""
        return [m.get("id") for m in self._extract_memes_list()]

    def _ids_as_str(self):
        """Return meme ids from the last list response as strings."""
        return [str(meme_id) for meme_id in self._extract_meme_ids()]

    @allure.step("Assert meme id exists in list")
    def check_meme_exists_in_list(self, meme_id):
        """Assert meme_id is present in the memes list.

        Comparison uses str() so int/str id variants still match.
        Strict id typing stays in check_response_id_is_correct.

        Args:
            meme_id: Expected meme identifier.

        Raises:
            AssertionError: If the list is empty or meme_id is absent.
        """
        ids = self._ids_as_str()
        assert len(ids) > 0, "Memes list is empty"
        assert str(meme_id) in ids, f"Meme id {meme_id} not found in list"

    @allure.step("Assert meme id is absent from list")
    def check_meme_not_exists_in_list(self, meme_id):
        """Assert meme_id is not present in the memes list.

        Args:
            meme_id: Meme identifier that must be absent.

        Raises:
            AssertionError: If meme_id is still present in the list.
        """
        ids = self._ids_as_str()
        assert str(meme_id) not in ids, (
            f"Meme id {meme_id} is still present in the list"
        )

    @allure.step("Assert meme in list has required BRD fields")
    def check_meme_list_contains_required_fields(self, meme_id):
        """Assert meme with meme_id exists in list and has required fields.

        Lookup normalizes id with str(); type contract is checked elsewhere.

        Args:
            meme_id: Expected meme identifier.

        Raises:
            AssertionError: If meme is missing or required fields are absent.
        """
        memes = self._extract_memes_list()
        assert len(memes) > 0, "Memes list is empty"

        target = str(meme_id)
        match = next(
            (m for m in memes if str(m.get("id")) == target),
            None,
        )
        assert match is not None, f"Meme id {meme_id} not found in list"

        missing = [f for f in REQUIRED_MEME_FIELDS if f not in match]
        assert not missing, (
            f"Meme id {meme_id} missing required fields: {missing}. "
            f"Actual keys: {list(match.keys())}"
        )

    @allure.step("Assert response id is int and matches expected")
    def check_response_id_is_correct(self, expected_id: Any) -> None:
        """Assert response id is int and equals expected_id.

        Args:
            expected_id: Expected meme id value.

        Raises:
            AssertionError: If id is missing, not int, or does not match.
        """
        self.check_response_is_json()
        body = self.json
        assert body is not None, "Response JSON body is None after parse"
        actual_id = body.get("id")
        assert isinstance(actual_id, int), (
            f"ID must be int, got {type(actual_id)} (value: {actual_id})"
        )
        assert actual_id == expected_id, (
            f"Response id mismatch. Expected: {expected_id}, got: {actual_id}"
        )
