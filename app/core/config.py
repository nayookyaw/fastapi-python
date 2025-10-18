from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "FastAPI Boilerplate"
    env:str = "dev"
    env_filename = ".env"

    db_user: str
    db_pass: str
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str

    @property
    def database_url(self) -> str:
        # Async SQLAlchemy + aiomysql URL
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    model_config = SettingsConfigDict(env_file=env_filename, env_prefix="", extra="ignore")

settings = Settings()