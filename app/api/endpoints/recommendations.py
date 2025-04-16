from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.recommendation import Recommendation
from app.services.recommendation import RecommendationService
from app.db.session import get_async_session
from app.core.auth.jwt import get_current_user

router = APIRouter()

@router.get(
    "/{recommendation_id}",
    response_model=Recommendation,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "timestamp": "2025-04-17T10:00:00Z",
                        "recommendation_text": "Physical Therapy"
                    }
                }
            }
        },
        404: {
            "description": "Recommendation not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Recommendation not found"}
                }
            }
        },
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        }
    },
    summary="Get a specific recommendation",
    description="""
    Retrieve a recommendation by its ID. Returns cached version if available.
    
    The endpoint requires authentication using JWT token.
    Recommendations are cached in Redis for improved performance.
    """
)
async def get_recommendation(
    recommendation_id: str,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> Recommendation:
    """
    Get a specific recommendation by ID.

    Args:
        recommendation_id: Unique identifier of the recommendation
        current_user: The currently authenticated user (injected by dependency)
        db: Database session (injected by dependency)

    Returns:
        Recommendation: The requested recommendation

    Raises:
        HTTPException: If recommendation not found (404)
    """
    service = RecommendationService(db)
    recommendation = await service.get_by_id(recommendation_id)
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    return recommendation