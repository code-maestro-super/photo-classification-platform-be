import pytest
from app.repositories.user_repository import get_user_by_email, get_user_by_id, create_user
from app.schemas.user import UserCreate
from app.core.security import verify_password


def test_create_user(db_session):
    user_data = UserCreate(email="newuser@example.com", password="password123")
    user = create_user(db_session, user_data)
    
    assert user.id is not None
    assert user.email == "newuser@example.com"
    assert verify_password("password123", user.password_hash)
    assert user.role.value == "user"


def test_get_user_by_email(db_session, test_user):
    user = get_user_by_email(db_session, "test@example.com")
    assert user is not None
    assert user.email == "test@example.com"


def test_get_user_by_email_not_found(db_session):
    user = get_user_by_email(db_session, "nonexistent@example.com")
    assert user is None


def test_get_user_by_id(db_session, test_user):
    user = get_user_by_id(db_session, test_user.id)
    assert user is not None
    assert user.id == test_user.id


def test_get_user_by_id_not_found(db_session):
    user = get_user_by_id(db_session, 99999)
    assert user is None

