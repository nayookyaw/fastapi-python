# app/db/create_db.py
from contextlib import asynccontextmanager
from typing import Tuple
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.engine.url import make_url, URL
from sqlalchemy import text
from app.core.db_config import db_settings

# --- helpers ---------------------------------------------------------------

def _admin_url(url: URL) -> URL:
    # Connect to the server without selecting your app DB.
    # Using database='mysql' avoids "Unknown database" on connect.
    return url.set(database="mysql")

def _render(url: URL) -> str:
    # Pretty-print the DSN without leaking the password
    return url.render_as_string(hide_password=True)

# --- engines (admin created now, app engine deferred) ----------------------

ADMIN_ENGINE: AsyncEngine | None = None
APP_ENGINE: AsyncEngine | None = None
DB_NAME: str | None = None

def _init_admin() -> Tuple[AsyncEngine, str, URL]:
    url = make_url(db_settings.database_url)
    admin = create_async_engine(
        _admin_url(url),
        isolation_level="AUTOCOMMIT",    # CREATE DATABASE cannot be in a txn
        pool_pre_ping=True,
    )
    return admin, (url.database or ""), url

async def _ensure_database_exists(admin: AsyncEngine, name: str):
    print(f"[lifespan] Ensuring database `{name}` exists…")
    async with admin.connect() as conn:
        await conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
    print("[lifespan] Database ensured.")

def _init_app_engine(url: URL) -> AsyncEngine:
    # Now safe to point at the real DB
    return create_async_engine(url, pool_pre_ping=True)

# --- FastAPI lifespan ------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ADMIN_ENGINE, APP_ENGINE, DB_NAME
    ADMIN_ENGINE, DB_NAME, full_url = _init_admin()
    print(f"[lifespan] admin DSN: {_render(_admin_url(full_url))}")
    print(f"[lifespan] app   DSN: {_render(full_url)}")
    try:
        # 1) Ensure DB exists (no tables/migrations here)
        await _ensure_database_exists(ADMIN_ENGINE, DB_NAME)

        # 2) Only now create the app engine that points to your DB
        APP_ENGINE = _init_app_engine(full_url)

        yield
    finally:
        # Clean shutdown
        if APP_ENGINE is not None:
            await APP_ENGINE.dispose()
        if ADMIN_ENGINE is not None:
            await ADMIN_ENGINE.dispose()
