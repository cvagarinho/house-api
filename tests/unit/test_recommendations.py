import uuid
from datetime import datetime

import pytest
from fastapi import status

from app.models.recommendation import RecommendationModel
from app.schemas.recommendation import Recommendation


@pytest.mark.asyncio
async def test_get_recommendation_success(
    async_client, auth_token, db_session, mock_redis
):
    """Test successful recommendation retrieval from database"""
    recommendation_id = str(uuid.uuid4())
    test_timestamp = datetime.now()

    # Create recommendation in database
    new_rec = RecommendationModel(
        id=recommendation_id,
        timestamp=test_timestamp,
        recommendation_text="Physical Therapy",
    )
    db_session.add(new_rec)
    await db_session.commit()

    # Ensure cache miss to hit database
    mock_redis["get"].return_value = None

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        f"/api/recommendations/{recommendation_id}", headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == recommendation_id
    assert data["timestamp"] == test_timestamp.isoformat()
    assert data["recommendation_text"] == "Physical Therapy"


@pytest.mark.asyncio
async def test_get_recommendation_not_found(async_client, auth_token, mock_redis):
    """Test recommendation not found"""
    mock_redis["get"].return_value = None

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        "/api/recommendations/nonexistent-id", headers=headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Recommendation not found"


@pytest.mark.asyncio
async def test_get_recommendation_unauthorized(async_client):
    """Test unauthorized access"""
    response = await async_client.get("/api/recommendations/123")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_recommendation_with_cache(async_client, auth_token, mock_redis):
    """Test recommendation retrieval from cache"""
    recommendation_id = str(uuid.uuid4())
    test_timestamp = "2025-04-17T10:00:00"
    
    cached_recommendation = Recommendation(
        id=recommendation_id,
        timestamp=test_timestamp,
        recommendation_text="Cached Recommendation"
    )
    
    # Convert to dict and ensure timestamp is string
    cached_data = {
        **cached_recommendation.model_dump(),
        "timestamp": cached_recommendation.timestamp.isoformat()
    }
    
    mock_redis["get"].return_value = cached_data

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        f"/api/recommendations/{recommendation_id}", headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    
    # Compare the response with our expected data
    assert response_data == cached_data
    mock_redis["get"].assert_called_once_with(f"recommendation:{recommendation_id}")


@pytest.mark.asyncio
async def test_get_recommendation_cache_miss(
    async_client, auth_token, db_session, mock_redis
):
    """Test recommendation retrieval from database after cache miss"""
    recommendation_id = str(uuid.uuid4())
    test_timestamp = datetime(2025, 4, 17, 10, 0)  # Use fixed timestamp for testing

    # Ensure cache miss
    mock_redis["get"].return_value = None

    # Create recommendation in DB
    new_rec = RecommendationModel(
        id=recommendation_id,
        timestamp=test_timestamp,
        recommendation_text="Physical Therapy",
    )
    db_session.add(new_rec)
    await db_session.commit()

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        f"/api/recommendations/{recommendation_id}", headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == recommendation_id
    assert data["timestamp"] == test_timestamp.isoformat()  # Compare with ISO format string
    assert data["recommendation_text"] == "Physical Therapy"

    # Verify cache interactions
    mock_redis["get"].assert_called_once_with(f"recommendation:{recommendation_id}")
    mock_redis["set"].assert_called_once()
