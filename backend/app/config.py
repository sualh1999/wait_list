from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    GMAIL_USER: str
    GMAIL_PASS: str
    ADMIN_PASSWORD: str
    ALLOWED_ORIGINS: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
