from fastapi import FastAPI

from app.api.routes import api_router
from app.cache.redis_manager import redis_manager
from app.db.init_db import initialize_database

app = FastAPI(
    title="House API",
    description="""
    Clinical Recommendations API with the following features:
    - JWT Authentication
    - Redis Caching
    - RabbitMQ Message Queue
    - PostgreSQL Database
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication operations. Register and login to obtain access token.",
        },
        {
            "name": "recommendations",
            "description": "Operations with clinical recommendations. Protected by JWT authentication.",
        },
        {
            "name": "evaluate",
            "description": "Patient evaluation endpoints. Generate recommendations based on patient data.",
        },
    ],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    await redis_manager.connect()
    await initialize_database()


@app.on_event("shutdown")
async def shutdown_event():
    await redis_manager.close()


@app.get("/")
async def root():
    return {"message": f"Welcome to House API. See /docs for API documentation."}
