from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "IFSO Cyber Helpdesk"
    APP_VERSION: str = "1.0.0"

    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./ifso.db"

    SECRET_KEY: str = "change-this-in-production"

    LOG_LEVEL: str = "INFO"

    DEFAULT_LANGUAGE: str = "en"

    SUPPORTED_LANGUAGES: str = "en,hi"

    SESSION_TIMEOUT: int = 1800

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def supported_languages(self) -> list[str]:
        return [
            language.strip()
            for language in self.SUPPORTED_LANGUAGES.split(",")
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()