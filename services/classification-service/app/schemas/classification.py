from pydantic import BaseModel
from typing import List, Dict, Any


class ClassificationResponse(BaseModel):
    category: str
    categories: List[str]
    confidence: float
    details: Dict[str, Any]

