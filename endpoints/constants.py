"""Environment config, HTTP status codes, and API path constants."""

import os
from dotenv import load_dotenv

load_dotenv()

# Secrets are loaded from environment / .env
BASE_URL = os.getenv("BASE_URL")
TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_TOKEN = os.getenv("TEST_TOKEN")

# HTTP status codes
STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404

AUTHORIZE_PATH = "/authorize"
MEME_PATH = "/meme"

CONTENT_TYPE_JSON = "application/json"
AUTHORIZATION_HEADER = "Authorization"

INVALID_AUTH_TOKEN = "wrong_token_1234567890"
