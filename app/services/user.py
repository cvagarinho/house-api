from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.auth.password import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Retrieve a user by email from the database.
    
    Args:
        db (AsyncSession): The database session
        email (str): Email to search for
        
    Returns:
        User | None: The user if found, otherwise None
    """
    result = await db.execute(
        select(User).filter(User.email == email)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user in the database.
    
    Args:
        db (AsyncSession): The database session
        user (UserCreate): The user data
        
    Returns:
        User: The created user
    """
    db_user = User(
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user