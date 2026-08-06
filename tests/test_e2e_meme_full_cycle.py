"""End-to-end meme lifecycle test."""

import pytest
import allure
from utils.data_generator import generate_meme_data


@allure.feature("End-to-End testing")
@allure.story("Integration scenario: full meme lifecycle")
class TestMemeFullLifecycle:
    """Full CRUD lifecycle for a single meme."""

    @allure.title("Full CRUD lifecycle for a meme")
    @pytest.mark.critical
    def test_complete_meme_lifecycle(
            self,
            meme_fixture,
            get_meme_by_id_endpoint,
            update_meme_endpoint,
            delete_meme_endpoint,
            get_all_memes_endpoint,
    ):
        """Create → list → get → update → get → delete → verify absence."""
        meme_id = meme_fixture["id"]
        original_data = meme_fixture["data"]
        updated_data = generate_meme_data()
        updated_data["id"] = meme_id

        with allure.step("Step 1: Verify meme is in the list (GET /meme)"):
            get_all_memes_endpoint.get_all_memes()
            get_all_memes_endpoint.check_meme_exists_in_list(meme_id)

        with allure.step("Step 2: Get meme by ID (GET /meme/{id})"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_id)
            get_meme_by_id_endpoint.check_successful_meme_response(
                original_data)

        with allure.step("Step 3: Update meme (PUT /meme/{id})"):
            update_meme_endpoint.update_meme(meme_id, updated_data)
            update_meme_endpoint.check_successful_meme_response(updated_data)

        with allure.step("Step 4: Verify changes via GET"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_id)
            get_meme_by_id_endpoint.check_successful_meme_response(
                updated_data)

        with allure.step("Step 5: Delete meme (DELETE /meme/{id})"):
            delete_meme_endpoint.delete_meme(meme_id)
            delete_meme_endpoint.check_status_is_200()

        with allure.step("Step 6: Verify deletion via GET (expect 404)"):
            get_meme_by_id_endpoint.get_meme_by_id(meme_id)
            get_meme_by_id_endpoint.check_status_is_404()

        with allure.step("Step 7: Verify meme is absent from the list"):
            get_all_memes_endpoint.get_all_memes()
            get_all_memes_endpoint.check_meme_not_exists_in_list(meme_id)

        meme_fixture["skip_cleanup"] = True
