from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.base_class import Base
from app.db.session import engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def initialize_database():
    await init_db()
