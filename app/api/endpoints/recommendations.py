from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.recommendation import Recommendation, RecommendationResponse
from app.services.recommendation import get_recommendation_by_id
from app.db.session import get_db

router = APIRouter()

@router.get("/{recommendation_id}", response_model=Recommendation)
def get_recommendation(
    recommendation_id: str,
    db: Session = Depends(get_db)
) -> Recommendation:
    recommendation = get_recommendation_by_id(db, recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation