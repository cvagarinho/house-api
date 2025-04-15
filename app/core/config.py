from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_queue: str

    redis_host: str
    redis_port: int
    redis_db: int
    redis_cache_ttl: int

    class Config:
        env_file = ".env.local"

settings = Settings()