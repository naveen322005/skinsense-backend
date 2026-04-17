from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from models.user import PyObjectId

class PredictionModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    image_url: Optional[str] = None
    primary_disease: str
    confidence_score: float
    top_3_predictions: List[dict]
    explanation: str
    recommendations: str
    avoid_ingredients: str
    safe_ingredients: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
