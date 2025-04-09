from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, recommendations
from app.core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Healthcare Recommendation API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(
    recommendations.router,
    prefix=f"{settings.API_V1_STR}/recommendations",
    tags=["recommendations"]
)