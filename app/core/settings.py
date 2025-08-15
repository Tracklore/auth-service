# Application settings (loading from .env)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Auth Service"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    database_url: str
    access_token_expire_minutes: int = 60 * 24 # 24 hours
    refresh_token_expire_minutes: int = 60 * 24 * 30 # 30 days
    algorithm: str = "HS256"
    rabbitmq_url: str = "amqp://guest:guest@localhost/"

settings = Settings()