from app.schemas.recommendation import PatientData, Recommendation
from app.models.recommendation import RecommendationModel
from sqlalchemy.orm import Session
from typing import List

def generate_recommendation(db: Session, patient_data: PatientData) -> Recommendation:
    """
    Generate clinical recommendations based on multiple rules.
    """
    recommendations = []
    
    if patient_data.age > 65 and patient_data.has_chronic_pain:
        recommendations.append("Physical Therapy.")
    
    if patient_data.bmi and patient_data.bmi > 30:
        recommendations.append("Weight Management Program.")
    
    if patient_data.recent_surgery:
        recommendations.append("Post-Op Rehabilitation Plan.")
    
    # If no recommendations were generated
    if not recommendations:
        recommendations.append("No specific recommendations at this time.")
    
    # Join all recommendations with line breaks
    recommendation_text = " ".join(recommendations)
    
    # Create database model
    db_recommendation = RecommendationModel(
        recommendation_text=recommendation_text
    )
    
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return Recommendation(
        id=db_recommendation.id,
        timestamp=db_recommendation.timestamp,
        recommendation_text=db_recommendation.recommendation_text
    )

def get_recommendation_by_id(db: Session, recommendation_id: str) -> RecommendationModel:
    """Retrieve a recommendation by ID."""
    return db.query(RecommendationModel).filter(RecommendationModel.id == recommendation_id).first()