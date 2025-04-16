from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.schemas.recommendation import PatientData, Recommendation
from app.services.recommendation import generate_recommendation

router = APIRouter()

@router.post(
    "/",
    response_model=Recommendation,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Successful evaluation",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "timestamp": "2025-04-17T10:00:00Z",
                        "recommendation_text": "Physical Therapy, Weight Management Program"
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "age"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    },
    summary="Evaluate patient data",
    description="""
    Generate clinical recommendations based on patient data.
    
    The recommendation will be:
    - Stored in the database
    - Published to RabbitMQ for processing
    - Cached in Redis for future retrievals
    """
)
async def evaluate_patient(
    patient_data: PatientData,
    db: AsyncSession = Depends(get_async_session)
) -> Recommendation:
    return await generate_recommendation(db, patient_data)

example_patient_data = {
    "age": 70,
    "bmi": 32.5,
    "has_chronic_pain": True,
    "recent_surgery": False
}