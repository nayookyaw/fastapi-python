from fastapi import FastAPI
from app.core.db_config import db_settings
from app.db.create_db import lifespan # import before routers
from app.routers.user_router import user_routers

app = FastAPI(title=db_settings.app_name, lifespan=lifespan)

# include routers
app.include_router(user_routers)