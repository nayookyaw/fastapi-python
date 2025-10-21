from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from fastapi import FastAPI
from app.core.db_config import db_settings

Base = declarative_base()

def build_engines(database_url: str) -> tuple[AsyncEngine, AsyncEngine, str]:
    url = make_url(database_url)
    db_name = "mysql"
    
    admin_url = url.set(database=None)
    admin_engine = create_async_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )
    app_engine = create_async_engine(database_url, pool_pre_ping=True)
    return admin_engine, app_engine, db_name

admin_engine, app_engine, database_name = build_engines(db_settings.database_url)

async def ensure_database_exists():
    async with admin_engine.connect() as conn:
        result = await conn.execute(
            text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db_name"),
            {"db_name": database_name},
        )
        exists = result.first() is not None
        if not exists:
            await conn.execute(text(f"CREATE DATABASE {database_name}"))
            print(f"Database '{database_name}' created.")
        else:
            print(f"Database '{database_name}' already exists.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ensure DB exists
    await ensure_database_exists()
    yield
    # optional: cleanup
    await admin_engine.dispose()
    await app_engine.dispose()