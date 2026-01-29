from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models.submission import Submission


def get_all_submissions(
    db: Session,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    location: Optional[str] = None,
    country: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> tuple[list[Submission], int]:
    query = db.query(Submission)
    
    if age is not None:
        query = query.filter(Submission.age == age)
    
    if gender:
        query = query.filter(Submission.gender.ilike(f"%{gender}%"))
    
    if location:
        query = query.filter(Submission.place_of_living.ilike(f"%{location}%"))
    
    if country:
        query = query.filter(Submission.country_of_origin.ilike(f"%{country}%"))
    
    if date_from:
        query = query.filter(Submission.created_at >= date_from)
    
    if date_to:
        query = query.filter(Submission.created_at <= date_to)
    
    total = query.count()
    
    sort_column = getattr(Submission, sort_by, Submission.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    submissions = query.offset(skip).limit(limit).all()
    
    return submissions, total


def get_submission_by_id(db: Session, submission_id: int) -> Optional[Submission]:
    return db.query(Submission).filter(Submission.id == submission_id).first()

