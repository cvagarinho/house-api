from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.recommendation import PatientData, Recommendation
from app.services.recommendation import generate_recommendation

router = APIRouter()

@router.post("/", response_model=Recommendation)
def evaluate_patient(
    patient_data: PatientData,
    db: Session = Depends(get_db)
) -> Recommendation:
    return generate_recommendation(db, patient_data)