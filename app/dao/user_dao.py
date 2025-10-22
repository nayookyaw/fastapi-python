from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class UserDao:
    def __init__(self):
        pass

    async def create_user(self, db: AsyncSession, *, email: str, password: str, full_name: str):
        user = User(
            email=email,
            password=password,
            full_name=full_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_email(self, db: AsyncSession, email: str):
        exist_user = await db.execute(select(User).where(User.email == email))
        return exist_user.scalar_one_or_none()