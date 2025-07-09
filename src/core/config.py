from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SYNC_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PYTHONPATH: str

    class Config:
        env_file = ".env"


settings = Settings()
