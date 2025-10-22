from fastapi import APIRouter
from app.schemas.user_schema import UserCreate
from app.controllers.user_controller import UserController

user_routers = APIRouter(prefix="/user", tags=["users"])

@user_routers.post("")
async def register(payload: UserCreate):
    return await UserController.register_user(user_data=payload)