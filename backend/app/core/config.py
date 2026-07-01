from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "HydroForecast"
    database_url: str = "postgresql+asyncpg://hydroforecast:hydroforecast_secret@postgres:5432/hydroforecast"
    secret_key: str = "hydroforecast-jwt-secret-change-in-production-8a7df9b2"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
