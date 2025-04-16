from app.db.base import Base
from app.db.session import engine


async def initialize_database():
    """Initialize the database and create all tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
