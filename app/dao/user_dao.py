from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.models.user import User

class UserDao:
    @classmethod
    async def create_user(cls, *, email: str, password: str, full_name: str | None) -> User:
        _db: AsyncSession = Depends(get_db)
        user: User = User(
            email=email,
            password=password,
            full_name=full_name,
        )
        _db.add(user)
        await _db.commit()
        await _db.refresh(user)
        return user

    @classmethod
    async def get_user_by_email(cls, email: str) -> User | None:
        _db: AsyncSession = Depends(get_db)
        exist_user = await _db.execute(select(User).where(User.email == email))
        return exist_user.scalar_one_or_none()