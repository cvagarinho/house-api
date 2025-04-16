from fastapi import FastAPI
from app.api.routes import api_router
from app.cache.redis_manager import redis_manager
from app.db.init_db import initialize_database

app = FastAPI(
    title="HOUSE API",
    description="API for generating and retrieving clinical recommendations",
    version="1.0.0",
    openapi_url="/house-api/openapi.json",
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