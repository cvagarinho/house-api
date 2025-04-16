from sqlalchemy import select
from app.services.base import BaseService
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.auth.password import get_password_hash

class UserService(BaseService):
    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(
            select(User).filter(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            password=get_password_hash(user.password)
        )
        self._db.add(db_user)
        await self._db.commit()
        await self._db.refresh(db_user)
        return db_user