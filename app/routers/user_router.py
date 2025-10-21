from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserGet
from app.dao.users import create_user, get_user_by_email

user_routers = APIRouter(prefix="/user", tags=["users"])

@user_routers.post("", response_model=UserGet, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    exit = await get_user_by_email(db, payload.email)
    if exit:
        raise HTTPException(status_code=409, detail="Email already registered")
    new_user = await create_user(db, email=payload.email, password=payload.password, full_name=payload.full_name)
    return new_user