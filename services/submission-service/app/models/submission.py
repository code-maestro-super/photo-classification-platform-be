from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False, index=True)
    place_of_living = Column(String, nullable=False, index=True)
    gender = Column(String, nullable=False, index=True)
    country_of_origin = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    photo_path = Column(String, nullable=False)
    classification_result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

