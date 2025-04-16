from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class PatientData(BaseModel):
    age: int = Field(
        ...,
        gt=0,
        description="Patient's age in years"
    )
    bmi: float = Field(
        ...,
        gt=0,
        description="Patient's Body Mass Index"
    )
    has_chronic_pain: bool = Field(
        ...,
        description="Whether patient has chronic pain"
    )
    recent_surgery: bool = Field(
        ...,
        description="Whether patient had recent surgery"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "age": 70,
                "bmi": 32.5,
                "has_chronic_pain": True,
                "recent_surgery": False
            }
        }

class Recommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    recommendation_text: str
    
    class Config:
        orm_mode = True
    
class RecommendationResponse(BaseModel):
    recommendation_id: str
    recommendation: Recommendation