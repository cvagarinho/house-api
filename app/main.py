from fastapi import FastAPI
from app.api.endpoints import recomendations

app = FastAPI(
    title="House MD API",
    description="Healthcare Recommendation API",
    version="0.1.0",
    openapi_url=f"/house-md/openapi.json"
)

app.include_router(recomendations.router, prefix="/recommendations", tags=["Recommendations"])
