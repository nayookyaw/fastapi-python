from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    app_name: str = "FastAPI Boilerplate"
    env:str = "dev"

    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: Optional[str] = None

    @property
    def database_url(self) -> str:
        # Async SQLAlchemy + asyncmy  URL
        if not (self.db_user and self.db_pass and self.db_name):
            # missing credentials/config — return empty string or handle as needed
            return ""
        return (
            f"mysql+asyncmy://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    # v2 way to point at your .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # optional:
        env_prefix="",     # e.g. "APP_" to read APP_DEBUG, APP_DATABASE_URL, ...
        extra="ignore",    # ignore unknown .env keys instead of erroring
    )

db_settings = DBSettings()