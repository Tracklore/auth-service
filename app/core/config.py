from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Auth Service"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # Database settings
    database_url: str
    
    # Message queue settings
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    
    # Environment-specific settings
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Create a cached instance of settings."""
    return Settings()