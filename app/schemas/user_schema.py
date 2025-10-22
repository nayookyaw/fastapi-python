from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr = Field (..., description="Must be a valid email address")
    password: str
    full_name: str | None = None

class UserScheme(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    model_config = {"from_attributes": True}