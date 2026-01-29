import pytest
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from datetime import timedelta


def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_create_access_token():
    data = {"sub": 1, "email": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)


def test_decode_access_token():
    data = {"sub": 1, "email": "test@example.com"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    
    assert payload is not None
    assert payload["sub"] == 1
    assert payload["email"] == "test@example.com"


def test_decode_invalid_token():
    payload = decode_access_token("invalid_token")
    assert payload is None

