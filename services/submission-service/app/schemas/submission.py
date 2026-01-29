from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SubmissionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=1, le=150)
    place_of_living: str = Field(..., min_length=1, max_length=100)
    gender: str = Field(..., min_length=1, max_length=50)
    country_of_origin: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)


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


class SubmissionList(BaseModel):
    items: list[SubmissionResponse]
    total: int

