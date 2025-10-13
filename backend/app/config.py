from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    RESEND_API_KEY: str
    ADMIN_PASSWORD: str
    ALLOWED_ORIGINS: str = ""

    model_config = SettingsConfigDict(env_file=None) # Explicitly disable .env file loading

settings = Settings()
