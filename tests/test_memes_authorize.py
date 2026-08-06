"""Authorization endpoint tests."""

import pytest
import allure
from conftest import create_endpoint_with_token
from endpoints.constants import (
    TEST_USERNAME,
    STATUS_BAD_REQUEST,
)
from endpoints.authorize import Authorize
from endpoints.get_all_memes import GetAllMemes


@pytest.fixture(scope="function")
def auth_api():
    """Fresh Authorize client per test."""
    return Authorize()


@allure.feature("Authorization")
@allure.story("Endpoint /authorize")
class TestMemesAuthorize:
    """Tests for /authorize flows."""

    @allure.title("Positive: authorize with a valid name")
    @pytest.mark.critical
    def test_authorize_valid_user(self, auth_api):
        """Authorize with a valid name and use the token on GET /meme."""
        auth_api.authorize(TEST_USERNAME)
        auth_api.check_status_is_200()
        auth_api.check_response_is_json()

        token = auth_api.json.get("token")
        user = auth_api.json.get("user")

        assert token, "Token is missing in the response"
        assert user == TEST_USERNAME, (
            f"Expected user {TEST_USERNAME}, got {user}"
        )

        with allure.step("Token grants access to protected GET /meme"):
            memes_api = create_endpoint_with_token(GetAllMemes, token)
            memes_api.get_all_memes()
            memes_api.check_status_is_200()
            memes_api.check_response_is_json()

    @allure.title("Check status of an existing token")
    @pytest.mark.medium
    def test_check_existing_token(self, auth_api, auth_token):
        """Alive token check returns expected message and username."""
        auth_api.get_token_status(auth_token)
        auth_api.check_status_is_200()
        response_text = auth_api.response.text
        assert "Token is alive" in response_text, (
            f"Unexpected response message: {response_text}"
        )
        assert TEST_USERNAME in response_text, (
            f"Username {TEST_USERNAME} not found in response: "
            f"{response_text}"
        )

    @allure.title("Negative: authorize with invalid name type")
    @pytest.mark.medium
    @pytest.mark.parametrize(
        "test_case",
        [
            {
                "description": "Name as null",
                "name": None,
                "expected_status": STATUS_BAD_REQUEST,
            },
            {
                "description": "Name as int",
                "name": 12345,
                "expected_status": STATUS_BAD_REQUEST,
            },
        ],
        ids=lambda x: x["description"],
    )
    def test_authorize_rejects_non_string_name(self, auth_api, test_case):
        """Reject authorize when name has an invalid type."""
        auth_api.authorize(test_case["name"])
        auth_api.check_status_code(test_case["expected_status"])

    @allure.title("Authorize with empty name (API accepts, user='')")
    @pytest.mark.medium
    def test_authorize_empty_name_accepted(self, auth_api):
        """Empty name is accepted by the API (observed contract)."""
        auth_api.authorize("")
        auth_api.check_status_is_200()
        auth_api.check_response_is_json()
        assert auth_api.json.get("token"), "Token is missing in the response"
        assert auth_api.json.get("user") == "", (
            f"Expected empty user, got: {auth_api.json.get('user')}"
        )

    @allure.title("Negative: authorize without name field")
    @pytest.mark.medium
    def test_authorize_missing_name_field(self, auth_api):
        """Reject authorize when name field is missing."""
        auth_api.authorize_with_payload({})
        auth_api.check_status_code(STATUS_BAD_REQUEST)

    @allure.title("Negative: check an invalid token")
    @pytest.mark.security
    def test_check_invalid_token(self, auth_api):
        """Unknown token check returns 404."""
        auth_api.get_token_status("invalid_token_12345")
        auth_api.check_status_is_404()

    @allure.title("Kill token: polling + deny access to /meme")
    @pytest.mark.security
    def test_kill_token_with_polling(self, auth_api):
        """Killed disposable token becomes 404 and cannot access GET /meme."""
        auth_api.authorize(f"{TEST_USERNAME}_kill")
        auth_api.check_status_is_200()
        killed_token = auth_api.json.get("token")
        assert killed_token, "Disposable token missing"

        auth_api.delete_token(killed_token)
        auth_api.check_status_is_200()
        auth_api.wait_until_deleted(killed_token)

        with allure.step("Killed token cannot access protected GET /meme"):
            memes_api = create_endpoint_with_token(GetAllMemes, killed_token)
            memes_api.get_all_memes()
            memes_api.check_status_is_401()
