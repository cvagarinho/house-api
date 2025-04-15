from redis import asyncio as aioredis
import json
from app.core.config import settings

class RedisManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        if self.redis is None:
            self.redis = await aioredis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                encoding="utf-8",
                decode_responses=True
            )

    async def get(self, key: str) -> dict:
        if not self.redis:
            await self.connect()
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int = None):
        if not self.redis:
            await self.connect()
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl or settings.redis_cache_ttl
        )

    async def close(self):
        if self.redis:
            await self.redis.close()

redis_manager = RedisManager()