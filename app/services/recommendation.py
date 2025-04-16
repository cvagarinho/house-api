from app.schemas.recommendation import PatientData, Recommendation
from app.models.recommendation import RecommendationModel
from app.messaging.publisher import RecommendationPublisher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def generate_recommendation(db: AsyncSession, patient_data: PatientData) -> Recommendation:
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
    
    if not recommendations:
        recommendations.append("No specific recommendations at this time.")
    
    recommendation_text = " ".join(recommendations)
    
    db_recommendation = RecommendationModel(
        recommendation_text=recommendation_text
    )
    
    db.add(db_recommendation)
    await db.commit()
    await db.refresh(db_recommendation)
    
    recommendation = Recommendation(
        id=db_recommendation.id,
        timestamp=db_recommendation.timestamp,
        recommendation_text=db_recommendation.recommendation_text
    )

    try:
        publisher = RecommendationPublisher()
        publisher.publish_recommendation(recommendation)
        publisher.close()
    except Exception as e:
        print(f"Failed to publish recommendation: {e}")

    return recommendation

async def get_recommendation_by_id(db: AsyncSession, recommendation_id: str) -> RecommendationModel:
    """
    Retrieve a recommendation by ID.

    Args:
        db (AsyncSession): The database session.
        recommendation_id (str): The ID of the recommendation to retrieve.

    Returns:
        RecommendationModel or None: The recommendation if found, otherwise None.
    """
    result = await db.execute(
        select(RecommendationModel).filter(RecommendationModel.id == recommendation_id)
    )
    return result.scalar_one_or_none()