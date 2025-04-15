from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class PatientData(BaseModel):
    age: int
    bmi: Optional[float] = None
    has_chronic_pain: bool = False
    recent_surgery: bool = False
    
class Recommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    recommendation_text: str
    
    class Config:
        orm_mode = True
    
class RecommendationResponse(BaseModel):
    recommendation_id: str
    recommendation: Recommendation