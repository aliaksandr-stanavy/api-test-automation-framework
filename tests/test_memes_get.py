"""GET /meme and GET /meme/<id> tests."""

import pytest
import allure
from endpoints.constants import INVALID_AUTH_TOKEN
from endpoints.get_all_memes import GetAllMemes
from endpoints.get_meme_by_id import GetMemeById
from utils.negative_test_cases import get_negative_test_cases_get


@allure.feature("Memes API")
@allure.story("GET operations")
class TestMemesGet:
    """Tests for reading memes."""

    @allure.title("Positive: get all memes")
    @pytest.mark.critical
    def test_get_all_memes(self, get_all_memes_endpoint, meme_fixture):
        """List memes and assert target meme has required BRD fields."""
        get_all_memes_endpoint.get_all_memes()
        get_all_memes_endpoint.check_status_is_200()
        get_all_memes_endpoint.check_meme_list_contains_required_fields(
            meme_fixture["id"]
        )

    @allure.title("Positive: get meme by ID")
    @pytest.mark.critical
    def test_get_meme_by_id(self, meme_fixture, get_meme_by_id_endpoint):
        """Fetch meme by id and validate payload plus id type."""
        meme_id = meme_fixture["id"]
        get_meme_by_id_endpoint.get_meme_by_id(meme_id)

        get_meme_by_id_endpoint.check_successful_meme_response(
            meme_fixture["data"])
        get_meme_by_id_endpoint.check_response_id_is_correct(meme_id)

    @allure.title("Negative GET cases: invalid IDs")
    @pytest.mark.medium
    @pytest.mark.parametrize("test_case", get_negative_test_cases_get(),
                             ids=lambda x: x["description"])
    def test_get_meme_negative_cases(self, get_meme_by_id_endpoint, test_case):
        """Return expected status for invalid meme ids."""
        get_meme_by_id_endpoint.get_meme_by_id(test_case["id"])
        get_meme_by_id_endpoint.check_status_code(test_case["expected_status"])

    @pytest.mark.security
    @pytest.mark.parametrize(
        "as_client",
        [
            (GetAllMemes, None),
            (GetAllMemes, INVALID_AUTH_TOKEN),
        ],
        indirect=True,
        ids=["no_token", "invalid_token"],
    )
    @allure.title("Security: list memes without a valid token")
    def test_get_all_memes_unauthorized(self, as_client):
        """Reject list access when Authorization is missing or invalid."""
        as_client.get_all_memes()
        as_client.check_status_is_401()

    @pytest.mark.security
    @pytest.mark.parametrize(
        "as_client",
        [
            (GetMemeById, None),
            (GetMemeById, INVALID_AUTH_TOKEN),
        ],
        indirect=True,
        ids=["no_token", "invalid_token"],
    )
    @allure.title("Security: get meme by ID without a valid token")
    def test_get_meme_by_id_unauthorized(self, as_client, meme_fixture):
        """Reject get-by-id when Authorization is missing or invalid."""
        as_client.get_meme_by_id(meme_fixture["id"])
        as_client.check_status_is_401()
