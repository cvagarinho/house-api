import pytest
from fastapi import status
from app.models.user import User
import uuid

@pytest.mark.asyncio
async def test_register_success(async_client, db_session):
    """Test successful user registration"""
    test_email = f"test_{uuid.uuid4()}@example.com"
    
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": test_email,
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_email
    assert "id" in data
    assert data["is_active"] is True

    # Verify user was created in database
    result = await db_session.get(User, data["id"])
    assert result is not None
    assert result.email == test_email

@pytest.mark.asyncio
async def test_register_duplicate_email(async_client):
    """Test registration with existing email"""
    test_email = f"test_{uuid.uuid4()}@example.com"
    
    # Register first user
    await async_client.post(
        "/api/auth/register",
        json={
            "email": test_email,
            "password": "password123"
        }
    )

    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": test_email,
            "password": "different123"
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_success(async_client, db_session):
    """Test successful login"""
    test_email = f"test_{uuid.uuid4()}@example.com"
    test_password = "password123"
    
    await async_client.post(
        "/api/auth/register",
        json={
            "email": test_email,
            "password": test_password
        }
    )

    response = await async_client.post(
        "/api/auth/token",
        data={
            "username": test_email,
            "password": test_password
        }
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client):
    """Test login with invalid credentials"""
    response = await async_client.post(
        "/api/auth/token",
        data={
            "username": f"wrong_{uuid.uuid4()}@example.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect email or password"

@pytest.mark.asyncio
async def test_register_invalid_email(async_client):
    """Test registration with invalid email format"""
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": "invalid_email",
            "password": "password123"
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "email"] and 
        error["type"] == "value_error"
        for error in errors
    )

@pytest.mark.asyncio
async def test_register_short_password(async_client):
    """Test registration with too short password"""
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": f"test_{uuid.uuid4()}@example.com",
            "password": "short"
        }
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "password"] 
        for error in errors
    )

