from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "House MD API"
    database_url: str

    class Config:
        env_file = ".env.local"

settings = Settings()