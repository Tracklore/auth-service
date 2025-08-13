# Application settings (loading from .env)
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(default="Auth Service", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
    database_url: str = Field(..., env="DATABASE_URL")
    access_token_expire_minutes: int = 60 * 24 # 24 hours
    refresh_token_expire_minutes: int = 60 * 24 * 30 # 30 days
    algorithm: str = "HS256"
    
    
    class Config:
        env_file = ".env"
        
settings = Settings()