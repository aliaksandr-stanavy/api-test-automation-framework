"""Pytest fixtures for Memes API automation."""

from collections.abc import Iterator
from typing import Any, TypeVar

import pytest
from endpoints import (
    TEST_TOKEN, TEST_USERNAME, STATUS_OK, STATUS_NOT_FOUND,
    Authorize, CreateMeme, GetAllMemes,
    GetMemeById, UpdateMeme, DeleteMeme
)
from endpoints.endpoint import Endpoint
from utils.data_generator import generate_meme_data

T = TypeVar("T", bound=Endpoint)


def create_endpoint_with_token(endpoint_class: type[T], token: str) -> T:
    """Create an endpoint client and attach an auth token.

    Args:
        endpoint_class: Endpoint class to instantiate.
        token: Authorization token string.

    Returns:
        Configured endpoint instance.
    """
    endpoint = endpoint_class()
    endpoint.set_token(token)
    return endpoint


@pytest.fixture(scope="session")
def auth_token() -> str:
    """Return a valid auth token, reusing TEST_TOKEN when still alive.

    Session-scoped: kill-token tests must use a disposable token, not this one.

    Returns:
        Authorization token string.
    """
    auth = Authorize()

    if TEST_TOKEN:
        check_response = auth.get_token_status(TEST_TOKEN)
        if check_response.status_code == STATUS_OK:
            return TEST_TOKEN

    response = auth.authorize(TEST_USERNAME)
    token = None
    if response.status_code == STATUS_OK and auth.json:
        token = auth.json.get("token")

    assert token is not None, "Failed to obtain authorization token"
    return token


@pytest.fixture(scope="function")
def create_meme_endpoint(auth_token: str) -> CreateMeme:
    """Authenticated CreateMeme client."""
    return create_endpoint_with_token(CreateMeme, auth_token)


@pytest.fixture(scope="function")
def get_all_memes_endpoint(auth_token: str) -> GetAllMemes:
    """Authenticated GetAllMemes client."""
    return create_endpoint_with_token(GetAllMemes, auth_token)


@pytest.fixture(scope="function")
def get_meme_by_id_endpoint(auth_token: str) -> GetMemeById:
    """Authenticated GetMemeById client."""
    return create_endpoint_with_token(GetMemeById, auth_token)


@pytest.fixture(scope="function")
def update_meme_endpoint(auth_token: str) -> UpdateMeme:
    """Authenticated UpdateMeme client."""
    return create_endpoint_with_token(UpdateMeme, auth_token)


@pytest.fixture(scope="function")
def delete_meme_endpoint(auth_token: str) -> DeleteMeme:
    """Authenticated DeleteMeme client."""
    return create_endpoint_with_token(DeleteMeme, auth_token)


@pytest.fixture()
def meme_fixture(
    create_meme_endpoint: CreateMeme, auth_token: str
) -> Iterator[dict[str, Any]]:
    """Create a meme for the test and delete it on teardown unless skipped.

    Yields:
        Dict with keys: id, data, response, skip_cleanup.
        Set skip_cleanup=True after the test deletes the meme itself.
    """
    meme_data = generate_meme_data()
    create_meme_endpoint.create_meme(meme_data)
    create_meme_endpoint.check_successful_meme_response(meme_data)

    meme_id = (
        create_meme_endpoint.json.get("id")
        if create_meme_endpoint.json
        else None
    )
    assert isinstance(meme_id, int), (
        f"meme_fixture setup: expected int id, got {meme_id!r}"
    )

    meme: dict[str, Any] = {
        "id": meme_id,
        "data": meme_data,
        "response": create_meme_endpoint.json,
        "skip_cleanup": False,
    }
    yield meme

    # Dedicated cleanup client so tests cannot clear auth on this path.
    # 200 and 404 are both OK when the test already deleted the meme.
    if meme_id and not meme.get("skip_cleanup"):
        cleanup = create_endpoint_with_token(DeleteMeme, auth_token)
        cleanup.delete_meme(meme_id)
        status = (
            cleanup.response.status_code
            if cleanup.response is not None
            else None
        )
        if status not in (STATUS_OK, STATUS_NOT_FOUND):
            pytest.fail(
                f"Teardown DELETE /meme/{meme_id} returned unexpected "
                f"status {status}"
            )


@pytest.fixture
def as_client(request: pytest.FixtureRequest) -> Endpoint:
    """Build an endpoint client from (endpoint_cls, token) params.

    Use with ``@pytest.mark.parametrize("as_client", [...], indirect=True)``.
    Pass ``token=None`` for a client without Authorization.

    Returns:
        Configured endpoint instance.
    """
    endpoint_cls, token = request.param
    client = endpoint_cls()
    if token is not None:
        client.set_token(token)
    return client


@pytest.fixture(scope="session")
def other_user_token() -> str:
    """Token for a second user (ownership / cross-user security tests).

    Returns:
        Authorization token string for ``{TEST_USERNAME}_other``.
    """
    auth = Authorize()
    other_name = f"{TEST_USERNAME}_other"
    auth.authorize(other_name)
    token = auth.json.get("token") if auth.json else None
    assert token, f"Failed to obtain token for {other_name}"
    return token


@pytest.fixture(scope="module")
def shared_meme_for_put_negatives(
    auth_token: str,
) -> Iterator[dict[str, Any]]:
    """Create one meme per module for PUT validation negatives.

    Status-only negative cases do not need a fresh resource each time.

    Yields:
        Dict with keys: id, data.
    """
    create = create_endpoint_with_token(CreateMeme, auth_token)
    meme_data = generate_meme_data()
    create.create_meme(meme_data)
    create.check_successful_meme_response(meme_data)

    meme_id = create.json.get("id") if create.json else None
    assert isinstance(meme_id, int), (
        f"shared_meme_for_put_negatives setup: expected int id, "
        f"got {meme_id!r}"
    )

    yield {"id": meme_id, "data": meme_data}

    cleanup = create_endpoint_with_token(DeleteMeme, auth_token)
    cleanup.delete_meme(meme_id)
    status = (
        cleanup.response.status_code
        if cleanup.response is not None
        else None
    )
    if status not in (STATUS_OK, STATUS_NOT_FOUND):
        pytest.fail(
            f"Teardown DELETE /meme/{meme_id} returned unexpected "
            f"status {status}"
        )
