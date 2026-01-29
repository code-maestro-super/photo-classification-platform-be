from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.core.storage import save_file
from app.core.http_client import call_classification_service
from app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionList
from app.repositories.submission_repository import (
    create_submission,
    get_submission_by_id,
    get_submissions_by_user,
    update_classification_result
)
import json

router = APIRouter(prefix="/api/v1/submissions", tags=["submissions"])


@router.post("", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission_endpoint(
    photo: UploadFile = File(...),
    metadata: str = Form(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        submission_data = SubmissionCreate(**json.loads(metadata))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid metadata: {str(e)}"
        )
    
    photo_path = await save_file(photo)
    
    submission = create_submission(db, user_id, submission_data, photo_path)
    
    classification_result = await call_classification_service(photo_path)
    if classification_result:
        result_str = json.dumps(classification_result)
        update_classification_result(db, submission.id, result_str)
        db.refresh(submission)
    
    return submission


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    submission = get_submission_by_id(db, submission_id, user_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    return submission


@router.get("", response_model=SubmissionList)
async def list_submissions(
    skip: int = 0,
    limit: int = 100,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    submissions, total = get_submissions_by_user(db, user_id, skip, limit)
    return SubmissionList(items=submissions, total=total)

