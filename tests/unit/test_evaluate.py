import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_evaluate_patient_success(async_client):
    """Test successful patient evaluation"""
    example_patient_data = {
        "age": 70,
        "bmi": 32.5,
        "has_chronic_pain": True,
        "recent_surgery": False,
    }

    response = await async_client.post("/api/evaluate/", json=example_patient_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert "timestamp" in data
    assert "recommendation_text" in data


@pytest.mark.asyncio
async def test_evaluate_patient_validation_error(async_client):
    """Test validation error response"""
    invalid_data = {
        "bmi": 32.5,
        "has_chronic_pain": True,
        "recent_surgery": False,
        # Missing required 'age' field
    }

    response = await async_client.post("/api/evaluate/", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    errors = response.json()["detail"]

    age_error = next(
        (error for error in errors if error["loc"] == ["body", "age"]), None
    )

    assert age_error is not None
    assert age_error["msg"] == "Field required"
    assert age_error["type"] == "missing"
