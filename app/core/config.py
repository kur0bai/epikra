from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str
    HUGGINGFACE_API_KEY: str
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
