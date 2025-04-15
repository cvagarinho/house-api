from fastapi import FastAPI
from app.api.routes import api_router
from app.db.init_db import init_db

app = FastAPI(
    title="HOUSE AI",
    description="API for generating and retrieving clinical recommendations",
    version="1.0.0",
    openapi_url="/house-api/openapi.json",
)

# Register API routes
app.include_router(api_router, prefix="/api")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": f"Welcome to House API. See /docs for API documentation."}