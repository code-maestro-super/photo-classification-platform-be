from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    name: str
    age: int
    place_of_living: str
    gender: str
    country_of_origin: str
    description: Optional[str]
    photo_path: str
    classification_result: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubmissionListResponse(BaseModel):
    items: List[SubmissionResponse]
    total: int
    page: int
    page_size: int

