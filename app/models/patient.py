from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Medication(BaseModel):
    name: str
    dosage: str
    frequency: str

class Condition(BaseModel):
    name: str
    diagnosed_date: Optional[date] = None
    severity: str = "moderate"

class PatientData(BaseModel):
    patient_id: str
    age: int = Field(..., gt=0, lt=120)
    gender: str
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    conditions: List[Condition] = []
    medications: List[Medication] = []
    allergies: List[str] = []
    vital_signs: Optional[dict] = None
    lab_results: Optional[dict] = None
    
    class Config:
        schema_extra = {
            "example": {
                "patient_id": "P12345",
                "age": 65,
                "gender": "male",
                "weight": 80.5,
                "height": 175.0,
                "conditions": [
                    {"name": "hypertension", "diagnosed_date": "2019-06-12", "severity": "moderate"},
                    {"name": "type 2 diabetes", "diagnosed_date": "2020-01-10", "severity": "mild"}
                ],
                "medications": [
                    {"name": "Lisinopril", "dosage": "10mg", "frequency": "daily"},
                    {"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"}
                ],
                "allergies": ["penicillin", "peanuts"],
                "vital_signs": {
                    "blood_pressure": "130/85",
                    "heart_rate": 72,
                    "temperature": 37.0
                },
                "lab_results": {
                    "hba1c": 7.1,
                    "cholesterol": 185
                }
            }
        }