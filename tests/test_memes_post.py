"""POST /meme tests."""

import copy

import pytest
import allure
from endpoints.constants import INVALID_AUTH_TOKEN
from endpoints.create_meme import CreateMeme
from utils.data_generator import (
    generate_meme_data,
    generate_minimal_meme_data,
    generate_maximal_meme_data
)
from utils.positive_test_cases import get_positive_test_cases
from utils.negative_test_cases import get_negative_test_cases_post


@allure.feature("Memes API")
@allure.story("POST operations")
class TestMemesPost:
    """Tests for creating memes."""

    @allure.title("Create meme (base case)")
    @pytest.mark.critical
    def test_create_meme_base(self, create_meme_endpoint,
                              get_meme_by_id_endpoint,
                              delete_meme_endpoint):
        """Create meme with base generated payload and verify via GET."""
        meme_data = generate_meme_data()
        meme_id = None
        try:
            create_meme_endpoint.create_meme(meme_data)
            create_meme_endpoint.check_successful_meme_response(meme_data)

            meme_id = create_meme_endpoint.json.get("id")
            assert isinstance(meme_id, int), (
                f"POST /meme must return id as int, "
                f"got {type(meme_id)} (value: {meme_id})"
            )

            with allure.step(f"Verify meme {meme_id} is available via GET"):
                get_meme_by_id_endpoint.get_meme_by_id(meme_id)
                get_meme_by_id_endpoint.check_successful_meme_response(
                    meme_data)
                get_meme_by_id_endpoint.check_response_id_is_correct(meme_id)
        finally:
            if meme_id is not None:
                delete_meme_endpoint.delete_meme(meme_id)

    @pytest.mark.parametrize(
        "generator_func",
        [
            pytest.param(
                generate_minimal_meme_data,
                id="Create meme with minimal data",
            ),
            pytest.param(
                generate_maximal_meme_data,
                id="Create meme with maximal data",
            ),
        ],
    )
    @allure.title("Create meme boundary sizes")
    @pytest.mark.medium
    def test_create_meme_boundary_sizes(self, create_meme_endpoint,
                                         get_meme_by_id_endpoint,
                                         delete_meme_endpoint, generator_func):
        """Create meme with minimal/maximal generated payloads."""
        meme_data = generator_func()
        meme_id = None
        try:
            create_meme_endpoint.create_meme(meme_data)
            create_meme_endpoint.check_successful_meme_response(meme_data)

            meme_id = create_meme_endpoint.json.get("id")
            assert isinstance(meme_id, int), (
                f"POST /meme must return id as int, "
                f"got {type(meme_id)} (value: {meme_id})"
            )

            with allure.step(f"Verify meme {meme_id} is available via GET"):
                get_meme_by_id_endpoint.get_meme_by_id(meme_id)
                get_meme_by_id_endpoint.check_successful_meme_response(
                    meme_data)
                get_meme_by_id_endpoint.check_response_id_is_correct(meme_id)
        finally:
            if meme_id is not None:
                delete_meme_endpoint.delete_meme(meme_id)

    @pytest.mark.parametrize("test_case", get_positive_test_cases(),
                             ids=lambda x: x["description"])
    @allure.title("Positive scenario: {test_case[description]}")
    @pytest.mark.medium
    def test_create_meme_positive_cases(self, create_meme_endpoint,
                                        delete_meme_endpoint, test_case):
        """Create meme from static positive cases and assert id type."""
        payload = copy.deepcopy(test_case["payload"])
        meme_id = None
        try:
            create_meme_endpoint.create_meme(payload)
            create_meme_endpoint.check_successful_meme_response(payload)
            meme_id = create_meme_endpoint.json.get("id")
            assert isinstance(meme_id, int), (
                f"POST /meme must return id as int, "
                f"got {type(meme_id)} (value: {meme_id})"
            )
        finally:
            if meme_id is not None:
                delete_meme_endpoint.delete_meme(meme_id)

    @pytest.mark.parametrize("test_case", get_negative_test_cases_post(),
                             ids=lambda x: x["description"])
    @allure.title("Negative scenario: {test_case[description]}")
    @pytest.mark.medium
    def test_create_meme_negative_validation(self, create_meme_endpoint,
                                             test_case):
        """Reject invalid create payloads with the expected status."""
        if test_case["raw_body"] is not None:
            create_meme_endpoint.create_meme(raw_body=test_case["raw_body"])
        else:
            create_meme_endpoint.create_meme(
                copy.deepcopy(test_case["payload"])
            )
        create_meme_endpoint.check_status_code(test_case["expected_status"])

    @pytest.mark.security
    @pytest.mark.parametrize(
        "as_client",
        [
            (CreateMeme, None),
            (CreateMeme, INVALID_AUTH_TOKEN),
        ],
        indirect=True,
        ids=["no_token", "invalid_token"],
    )
    @allure.title("Security: create meme without a valid token")
    def test_create_meme_unauthorized(self, as_client):
        """Reject create when Authorization is missing or invalid."""
        as_client.create_meme(generate_meme_data())
        as_client.check_status_is_401()
