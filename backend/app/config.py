from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "development"

    secret_key: str = "changeme"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    database_url: str  # async, for the running app
    sqlalchemy_database_url: str  # sync, for Alembic migrations

    redis_url: str

    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()