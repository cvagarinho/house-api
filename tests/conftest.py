from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import get_async_session
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def test_db_engine():
    engine = create_async_engine(DATABASE_URL, future=True, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_db_engine):
    async_session = async_sessionmaker(test_db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def async_client(db_session):
    """Async client fixture with overridden dependencies"""
    app.dependency_overrides[get_async_session] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def auth_token(async_client) -> str:
    """Create a test user and return its token"""
    await async_client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )

    response = await async_client.post(
        "/api/auth/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture
async def mock_redis(mocker):
    """Mock Redis with fresh mock objects for each test"""
    redis_get = AsyncMock(return_value=None)
    redis_set = AsyncMock()

    mocker.patch("app.cache.redis_manager.redis_manager.get", redis_get)
    mocker.patch("app.cache.redis_manager.redis_manager.set", redis_set)

    return {"get": redis_get, "set": redis_set}
