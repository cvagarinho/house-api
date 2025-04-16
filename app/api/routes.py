from fastapi import APIRouter

from app.api.endpoints import auth, evaluate, recommendations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(evaluate.router, prefix="/evaluate", tags=["evaluate"])

api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)
