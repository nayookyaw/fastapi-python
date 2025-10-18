from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def create_user(db: AsyncSession, *, email: str, password: str, full_name: str):
    user = User(
        email=email,
        password=password,
        full_name=full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
    