from fastapi import APIRouter
from app.api.endpoints import recommendations, evaluate

api_router = APIRouter()
api_router.include_router(
    evaluate.router,
    prefix="/evaluate",
    tags=["evaluate"]
)
api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["recommendations"]
)