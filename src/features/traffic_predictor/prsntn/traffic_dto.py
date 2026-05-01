from pydantic import BaseModel, Field
from typing import Optional

class TrafficPredictionRequest(BaseModel):
    datetime: str = Field(..., example="2026-03-29T18:00:00")
    road: str = Field(..., example="Bombo Road")

class TrafficPredictionResponse(BaseModel):
    road: str
    congestion: str
    confidence: float