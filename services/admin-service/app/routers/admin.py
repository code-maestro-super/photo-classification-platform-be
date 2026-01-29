from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.admin import SubmissionResponse, SubmissionListResponse
from app.repositories.submission_repository import get_all_submissions, get_submission_by_id

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/submissions", response_model=SubmissionListResponse)
async def list_submissions(
    age: Optional[int] = Query(None, description="Filter by age"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    location: Optional[str] = Query(None, description="Filter by place of living"),
    country: Optional[str] = Query(None, description="Filter by country of origin"),
    date_from: Optional[datetime] = Query(None, description="Filter from date (ISO format)"),
    date_to: Optional[datetime] = Query(None, description="Filter to date (ISO format)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=1000, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    admin: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    
    submissions, total = get_all_submissions(
        db=db,
        age=age,
        gender=gender,
        location=location,
        country=country,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return SubmissionListResponse(
        items=submissions,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
async def get_submission_details(
    submission_id: int,
    admin: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    submission = get_submission_by_id(db, submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    return submission

