from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.recommendation import Recommendation
from app.cache.redis_manager import redis_manager
from app.db.session import get_async_session
from app.services.recommendation import get_recommendation_by_id

router = APIRouter()

@router.get("/{recommendation_id}", response_model=Recommendation)
async def get_recommendation(
    recommendation_id: str,
    db: AsyncSession = Depends(get_async_session)
) -> Recommendation:
    
    cache_key = f"recommendation:{recommendation_id}"
    cached_data = await redis_manager.get(cache_key)
    
    if cached_data:
        return cached_data
    
    recommendation = await get_recommendation_by_id(db, recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    recommendation_data = Recommendation(
        id=recommendation.id,
        timestamp=recommendation.timestamp,
        recommendation_text=recommendation.recommendation_text
    )
    
    await redis_manager.set(cache_key, recommendation_data)
    
    return recommendation_data