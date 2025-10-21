from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# import all models here
from app.models.user import User