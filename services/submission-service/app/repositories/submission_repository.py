from sqlalchemy.orm import Session
from typing import Optional
from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate


def create_submission(db: Session, user_id: int, submission_data: SubmissionCreate, photo_path: str) -> Submission:
    db_submission = Submission(
        user_id=user_id,
        name=submission_data.name,
        age=submission_data.age,
        place_of_living=submission_data.place_of_living,
        gender=submission_data.gender,
        country_of_origin=submission_data.country_of_origin,
        description=submission_data.description,
        photo_path=photo_path
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_submission_by_id(db: Session, submission_id: int, user_id: Optional[int] = None) -> Optional[Submission]:
    query = db.query(Submission).filter(Submission.id == submission_id)
    if user_id:
        query = query.filter(Submission.user_id == user_id)
    return query.first()


def get_submissions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> tuple[list[Submission], int]:
    submissions = db.query(Submission).filter(Submission.user_id == user_id).offset(skip).limit(limit).all()
    total = db.query(Submission).filter(Submission.user_id == user_id).count()
    return submissions, total


def update_classification_result(db: Session, submission_id: int, result: str) -> Optional[Submission]:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission:
        submission.classification_result = result
        db.commit()
        db.refresh(submission)
    return submission

