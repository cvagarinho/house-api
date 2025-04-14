from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/evaluate")
async def evaluate(data):
    age = data.get("age")
    has_chronic_pain = data.get("has_chronic_pain", False)
    bmi = data.get("bmi")
    recent_surgery = data.get("recent_surgery", False)

    recommendations = []

    if age and age > 65 and has_chronic_pain:
        recommendations.append("Physical Therapy")
    if bmi and bmi > 30:
        recommendations.append("Weight Management Program")
    if recent_surgery:
        recommendations.append("Post-Op Rehabilitation Plan")

    return {"recommendations": recommendations}