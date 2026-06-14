from jose import jwt

from app.config import settings
from app.services.auth import (
    create_access_token,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_create_access_token():
    token = create_access_token("user1", "viewer")
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    assert payload["sub"] == "user1"
    assert payload["role"] == "viewer"
