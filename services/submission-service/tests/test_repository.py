import pytest
from app.repositories.submission_repository import (
    create_submission,
    get_submission_by_id,
    get_submissions_by_user,
    update_classification_result
)
from app.schemas.submission import SubmissionCreate


def test_create_submission(db_session, test_user):
    submission_data = SubmissionCreate(
        name="Test User",
        age=25,
        place_of_living="Test City",
        gender="Male",
        country_of_origin="Test Country",
        description="Test description"
    )
    submission = create_submission(db_session, test_user.id, submission_data, "/test/path.jpg")
    
    assert submission.id is not None
    assert submission.user_id == test_user.id
    assert submission.name == "Test User"
    assert submission.age == 25


def test_get_submission_by_id(db_session, test_submission):
    submission = get_submission_by_id(db_session, test_submission.id)
    assert submission is not None
    assert submission.id == test_submission.id


def test_get_submission_by_id_with_user_filter(db_session, test_submission, test_user):
    submission = get_submission_by_id(db_session, test_submission.id, test_user.id)
    assert submission is not None
    
    submission = get_submission_by_id(db_session, test_submission.id, 999)
    assert submission is None


def test_get_submissions_by_user(db_session, test_user, test_submission):
    submissions, total = get_submissions_by_user(db_session, test_user.id)
    assert total >= 1
    assert len(submissions) >= 1
    assert submissions[0].user_id == test_user.id


def test_update_classification_result(db_session, test_submission):
    result = '{"category": "test", "confidence": 0.9}'
    updated = update_classification_result(db_session, test_submission.id, result)
    
    assert updated is not None
    assert updated.classification_result == result

