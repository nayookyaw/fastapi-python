from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserGet(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    model_config = {"from_attributes": True}