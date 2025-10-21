from fastapi import FastAPI
from app.core.db_config import db_settings
from app.routers.user_router import user_routers
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title=db_settings.app_name)

# include routers
app.include_router(user_routers)

# create table at startup (for demo only, production should use Alembic migration)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)