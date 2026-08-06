"""DELETE /meme/<id> tests."""

import pytest
import allure
from conftest import create_endpoint_with_token
from endpoints.constants import INVALID_AUTH_TOKEN
from endpoints.delete_meme import DeleteMeme
from utils.negative_test_cases import get_negative_test_cases_delete


@allure.feature("Memes API")
@allure.story("DELETE operations")
class TestMemesDelete:
    """Tests for deleting memes."""

    @allure.title("Positive: delete a meme")
    @pytest.mark.critical
    def test_delete_meme(self, delete_meme_endpoint, get_meme_by_id_endpoint,
                         meme_fixture):
        """Delete a meme and verify it is gone via GET."""
        meme_id = meme_fixture["id"]

        with allure.step(f"Delete meme id {meme_id}"):
            delete_meme_endpoint.delete_meme(meme_id)
            delete_meme_endpoint.check_status_is_200()

        with allure.step("GET deleted meme expects 404"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_id)
            get_meme_by_id_endpoint.check_status_is_404()

        meme_fixture["skip_cleanup"] = True

    @allure.title("Negative DELETE cases: invalid IDs")
    @pytest.mark.medium
    @pytest.mark.parametrize(
        "test_case",
        get_negative_test_cases_delete(),
        ids=lambda x: x["description"],
    )
    def test_delete_meme_invalid_ids(self, delete_meme_endpoint, test_case):
        """Return expected status for invalid meme ids."""
        delete_meme_endpoint.delete_meme(test_case["id"])
        delete_meme_endpoint.check_status_code(test_case["expected_status"])

    @pytest.mark.security
    @pytest.mark.parametrize(
        "as_client",
        [
            (DeleteMeme, None),
            (DeleteMeme, INVALID_AUTH_TOKEN),
        ],
        indirect=True,
        ids=["no_token", "invalid_token"],
    )
    @allure.title("Security: delete meme without a valid token")
    def test_delete_meme_unauthorized(
            self, as_client, meme_fixture, get_meme_by_id_endpoint):
        """Reject delete when Authorization is missing or invalid."""
        meme_id = meme_fixture["id"]
        as_client.delete_meme(meme_id)
        as_client.check_status_is_401()

        with allure.step("Meme still exists after unauthorized delete"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_id)
            get_meme_by_id_endpoint.check_status_is_200()

    @allure.title("Security: other user cannot delete meme")
    @pytest.mark.security
    def test_delete_meme_forbidden_for_other_user(
            self, meme_fixture, other_user_token, get_meme_by_id_endpoint):
        """Reject DELETE when caller is not the meme owner (403)."""
        meme_id = meme_fixture["id"]
        client = create_endpoint_with_token(DeleteMeme, other_user_token)
        client.delete_meme(meme_id)
        client.check_status_is_403()

        with allure.step("Meme still exists after forbidden delete"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_id)
            get_meme_by_id_endpoint.check_status_is_200()

    @allure.title("Negative: double delete of the same meme")
    @pytest.mark.medium
    def test_double_delete(self, delete_meme_endpoint, meme_fixture):
        """Second delete of the same id returns 404."""
        meme_id = meme_fixture["id"]

        delete_meme_endpoint.delete_meme(meme_id)
        delete_meme_endpoint.check_status_is_200()

        delete_meme_endpoint.delete_meme(meme_id)
        delete_meme_endpoint.check_status_is_404()

        meme_fixture["skip_cleanup"] = True
