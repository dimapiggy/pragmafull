# backend/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field  # Добавьте этот импорт
from datetime import timedelta


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str

    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    
    # УДАЛИТЬ старый class Config и использовать только model_config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


class TelegramBotSettings(BaseSettings):
    telegram_bot_token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


class AuthSettings(BaseSettings):
    jwt_access_secret: str
    jwt_refresh_secret: str
    access_expire_minutes: int = 60  # Значение по умолчанию
    refresh_expire_days: int = 30    # Значение по умолчанию

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    @property
    def access_expire(self) -> timedelta:
        return timedelta(minutes=self.access_expire_minutes)

    @property
    def refresh_expire(self) -> timedelta:
        return timedelta(days=self.refresh_expire_days)


settings = Settings()
telegram_settings = TelegramBotSettings()
auth_settings = AuthSettings()