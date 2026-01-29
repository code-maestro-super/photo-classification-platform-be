import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app
from app.models.submission import Submission
from app.models.user import User
from app.core.security import get_password_hash
import tempfile
import os


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def temp_upload_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["UPLOAD_DIR"] = tmpdir
        yield tmpdir


@pytest.fixture(scope="function")
def client(db_session, temp_upload_dir):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    class User:
        def __init__(self):
            self.id = 1
            self.email = "test@example.com"
            self.role = "user"
    
    return User()


@pytest.fixture
def test_submission(db_session, test_user):
    submission = Submission(
        user_id=test_user.id,
        name="Test User",
        age=25,
        place_of_living="Test City",
        gender="Male",
        country_of_origin="Test Country",
        description="Test description",
        photo_path="/test/path.jpg"
    )
    db_session.add(submission)
    db_session.commit()
    db_session.refresh(submission)
    return submission


@pytest.fixture
def auth_token(client, test_user):
    from jose import jwt
    from app.core.config import settings
    
    token = jwt.encode(
        {"sub": test_user.id, "email": test_user.email, "role": test_user.role},
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return token

