from fastapi import FastAPI, Request
from app.core.db_config import db_settings
from app.db.create_db import lifespan # import before routers
from app.routers.user_router import user_routers
from fastapi.exceptions import RequestValidationError
from app.response_handlers.validation_handler import validation_exception_handler

app = FastAPI(title=db_settings.app_name, lifespan=lifespan)

# include routers
app.include_router(user_routers)

app.add_exception_handler(RequestValidationError,validation_exception_handler)