from app.models.user import User
from app.response_handlers.json_response_handler import Response_200, Response_400
from app.schemas.user_schema import UserCreate, UserScheme
from app.dao.user_dao import UserDao

class UserController:
    @classmethod
    async def register_user(cls, user_data: UserCreate):
        exist_user: User | None = await UserDao.get_user_by_email(email=user_data.email)
        # if a user with this email already exists, return a 400 error
        if exist_user is not None:
            return Response_400(error="Email already registered", data=None)
        
        # create and return the newly registered user
        new_user: User = await UserDao.create_user(email=user_data.email, password=user_data.password, full_name=user_data.full_name)
        user_scheme : UserScheme = UserScheme.model_validate(new_user)
        return Response_200[UserScheme](message="User registered successfully", data=user_scheme)