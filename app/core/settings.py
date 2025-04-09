import os
from typing import List
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "House MD API"
    
    # CORS
    ALLOWED_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000"]
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "very-secure-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./healthcare_app.db")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    
    class Config:
        env_file = ".env"

settings = Settings()