from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.schemas.recommendation import PatientData, Recommendation
from app.services.recommendation import generate_recommendation

router = APIRouter()

@router.post("/", response_model=Recommendation)
async def evaluate_patient(
    patient_data: PatientData,
    db: AsyncSession = Depends(get_async_session)
) -> Recommendation:
    return await generate_recommendation(db, patient_data)