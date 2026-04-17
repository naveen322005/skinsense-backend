from pydantic import BaseModel, Field
from typing import List

class PredictionResult(BaseModel):
    primary_disease: str
    confidence_score: float
    top_3_predictions: List[dict]
    explanation: str
    recommendations: str
    avoid_ingredients: str
    safe_ingredients: str

class PredictionOut(PredictionResult):
    id: str
    user_id: str
    image_url: str | None = None
    created_at: str

    class Config:
        from_attributes = True
