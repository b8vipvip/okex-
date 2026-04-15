from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Recharge Task API"
    app_env: str = "dev"
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    database_url: str
    redis_url: str = "redis://127.0.0.1:6379/0"

    admin_username: str = "admin"
    admin_password: str = "admin123"
    admin_token: str = "admin-token"
    worker_token: str = "worker-token"
    jwt_secret: str = "jwt-secret"
    access_token_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
