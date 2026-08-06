"""PUT /meme/<id> tests."""

import copy

import pytest
import allure
from conftest import create_endpoint_with_token
from endpoints.constants import INVALID_AUTH_TOKEN
from endpoints.update_meme import UpdateMeme
from utils.data_generator import generate_meme_data
from utils.positive_test_cases import get_positive_test_cases
from utils.negative_test_cases import get_negative_test_cases_put


@allure.feature("Memes API")
@allure.story("PUT operations")
class TestMemesUpdate:
    """Tests for updating memes."""

    @allure.title("Positive: update meme (smoke)")
    @pytest.mark.critical
    def test_update_meme_base(self, meme_fixture, update_meme_endpoint):
        """Update an existing meme with a generated payload."""
        meme_id = meme_fixture["id"]
        data = generate_meme_data()
        data["id"] = meme_id

        update_meme_endpoint.update_meme(meme_id, data)
        update_meme_endpoint.check_successful_meme_response(data)

    @pytest.mark.parametrize("test_case", get_positive_test_cases(),
                             ids=lambda x: x["description"])
    @allure.title("Positive update scenario: {test_case[description]}")
    @pytest.mark.medium
    def test_update_meme_positive_cases(self, meme_fixture,
                                        update_meme_endpoint, test_case):
        """Update an existing meme with a boundary/tolerance payload."""
        data = copy.deepcopy(test_case["payload"])
        meme_id = meme_fixture["id"]
        data["id"] = meme_id

        update_meme_endpoint.update_meme(meme_id, data)
        update_meme_endpoint.check_successful_meme_response(data)

    @pytest.mark.medium
    @pytest.mark.xfail(
        reason=(
            "Known API bug: PUT /meme/<id> returns id as string, "
            "but BRD requires id: int"
        ),
        strict=True,
    )
    @allure.title("Check ID type on update (PUT)")
    def test_update_meme_response_id_is_int(self, meme_fixture,
                                            update_meme_endpoint):
        """Assert PUT response id stays int and matches path id."""
        meme_id = meme_fixture["id"]
        update_data = {
            "id": meme_id,
            "text": "Checking ID type bug",
            "url": "https://example.com/meme.jpg",
            "tags": ["test"],
            "info": {"key": "value"}
        }

        update_meme_endpoint.update_meme(meme_id, update_data)
        update_meme_endpoint.check_response_id_is_correct(meme_id)

    @allure.title("Negative: update a non-existent meme")
    @pytest.mark.medium
    def test_update_nonexistent_meme(self, update_meme_endpoint):
        """Return 404 when updating a non-existent meme id."""
        update_data = generate_meme_data()
        invalid_id = 99999999
        update_data["id"] = invalid_id

        update_meme_endpoint.update_meme(invalid_id, update_data)
        update_meme_endpoint.check_status_is_404()

    @pytest.mark.parametrize("test_case", get_negative_test_cases_put(),
                             ids=lambda x: x["description"])
    @allure.title("Negative validation scenario: {test_case[description]}")
    @pytest.mark.medium
    def test_update_meme_negative_validation(
            self, shared_meme_for_put_negatives, update_meme_endpoint,
            test_case):
        """Reject invalid update payloads with the expected status."""
        meme_id = shared_meme_for_put_negatives["id"]

        if test_case["raw_body"] is not None:
            update_meme_endpoint.update_meme(
                meme_id, raw_body=test_case["raw_body"]
            )
        else:
            data = copy.deepcopy(test_case["payload"])
            if test_case["inject_id"]:
                data["id"] = meme_id
            update_meme_endpoint.update_meme(meme_id, data)

        update_meme_endpoint.check_status_code(test_case["expected_status"])

    @pytest.mark.security
    @pytest.mark.parametrize(
        "as_client",
        [
            (UpdateMeme, None),
            (UpdateMeme, INVALID_AUTH_TOKEN),
        ],
        indirect=True,
        ids=["no_token", "invalid_token"],
    )
    @allure.title("Security: update meme without a valid token")
    def test_update_meme_unauthorized(
            self, as_client, meme_fixture, get_meme_by_id_endpoint):
        """Reject update when Authorization is missing or invalid."""
        update_data = generate_meme_data()
        update_data["id"] = meme_fixture["id"]
        as_client.update_meme(meme_fixture["id"], update_data)
        as_client.check_status_is_401()

        with allure.step("Meme data unchanged after unauthorized update"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_fixture["id"])
            get_meme_by_id_endpoint.check_successful_meme_response(
                meme_fixture["data"])

    @allure.title("Security: other user cannot update meme")
    @pytest.mark.security
    def test_update_meme_forbidden_for_other_user(
            self, meme_fixture, other_user_token, get_meme_by_id_endpoint):
        """Reject PUT when caller is not the meme owner (403)."""
        client = create_endpoint_with_token(UpdateMeme, other_user_token)
        update_data = generate_meme_data()
        update_data["id"] = meme_fixture["id"]
        client.update_meme(meme_fixture["id"], update_data)
        client.check_status_is_403()

        with allure.step("Meme data unchanged after forbidden update"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_fixture["id"])
            get_meme_by_id_endpoint.check_successful_meme_response(
                meme_fixture["data"])
