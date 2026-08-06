"""Faker-based meme payload generators for critical happy-path tests."""

import faker
import random

from .types import MemePayload

fake = faker.Faker()


def generate_meme_data() -> MemePayload:
    """Generate a random valid meme payload.

    Returns:
        Dict with text, url, tags, and info.
    """
    tags = [fake.word() for _ in range(random.randint(1, 5))]
    info = {
        fake.word(): [fake.word() for _ in range(random.randint(1, 5))]
        for _ in range(random.randint(1, 3))
    }

    return {
        "text": fake.sentence(nb_words=random.randint(3, 10)),
        "url": fake.image_url(),
        "tags": tags,
        "info": info,
    }


def generate_minimal_meme_data() -> MemePayload:
    """Generate a minimal valid meme payload.

    Returns:
        Dict with short required fields.
    """
    return {
        "text": "a",
        "url": "http://a.co",
        "tags": ["t"],
        "info": {"k": ["v"]},
    }


def generate_maximal_meme_data() -> MemePayload:
    """Generate a larger valid meme payload.

    Returns:
        Dict with richer text/tags/info content.
    """
    return {
        "text": fake.sentence(nb_words=15),
        "url": fake.image_url(),
        "tags": [fake.word() for _ in range(5)],
        "info": {
            f"key{i}": [fake.word() for _ in range(5)] for i in range(5)
        },
    }
