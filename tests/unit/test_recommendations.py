import uuid
from datetime import datetime

import pytest
from fastapi import status

from app.models.recommendation import RecommendationModel


@pytest.mark.asyncio
async def test_get_recommendation_success(
    async_client, auth_token, db_session, mock_redis
):
    """Test successful recommendation retrieval from database"""
    recommendation_id = str(uuid.uuid4())

    # Create recommendation in database
    new_rec = RecommendationModel(
        id=recommendation_id,
        timestamp=datetime.now(),
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
    assert data["recommendation_text"] == "Physical Therapy"


@pytest.mark.asyncio
async def test_get_recommendation_not_found(async_client, auth_token, mock_redis):
    """Test recommendation not found"""
    mock_redis["get"].return_value = None

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        f"/api/recommendations/nonexistent-id", headers=headers
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
    cached_data = {
        "id": recommendation_id,
        "timestamp": "2025-04-17T10:00:00Z",
        "recommendation_text": "Cached Recommendation",
    }

    # Set up cache hit
    mock_redis["get"].return_value = cached_data

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await async_client.get(
        f"/api/recommendations/{recommendation_id}", headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == cached_data
    mock_redis["get"].assert_called_once_with(f"recommendation:{recommendation_id}")


@pytest.mark.asyncio
async def test_get_recommendation_cache_miss(
    async_client, auth_token, db_session, mock_redis
):
    """Test recommendation retrieval from database after cache miss"""
    recommendation_id = str(uuid.uuid4())

    # Ensure cache miss
    mock_redis["get"].return_value = None

    # Create recommendation in DB
    new_rec = RecommendationModel(
        id=recommendation_id,
        timestamp=datetime.now(),
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
    assert data["recommendation_text"] == "Physical Therapy"

    # Verify cache interactions
    mock_redis["get"].assert_called_once_with(f"recommendation:{recommendation_id}")
    mock_redis["set"].assert_called_once()
