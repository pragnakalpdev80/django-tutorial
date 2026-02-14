from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError


class Settings(BaseSettings):
    DEBUG: bool = Field(..., description="Debug mode")

    SECRET_KEY: str = Field(..., min_length=20)

    DB_NAME: str = Field(...)
    DB_USER: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_HOST: str = Field(...)
    DB_PORT: int = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


try:
    settings = Settings()
except ValidationError as e:
    print("\n❌ Environment configuration error:\n")
    print(e)
    raise SystemExit(1)
