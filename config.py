from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    """Все настройки приложения.

    Приоритет (от высшего к низшему):
      1. Переменные окружения (os.environ)
      2. Файл .env в корне проекта
      3. Значения по умолчанию ниже

    Аналог spf13/viper для Python.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ── Сервер ────────────────────────────────────────────────
    port: int = 5000
    flask_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # ── Безопасность ──────────────────────────────────────────
    secret_key: str = "dev-secret-change-in-production"

    # ── База данных ───────────────────────────────────────────
    database_url: str = f"sqlite:///{BASE_DIR / 'app.db'}"


# Единственный экземпляр — читается один раз при старте приложения
settings = Settings()


class Config:
    SECRET_KEY = settings.secret_key
    SQLALCHEMY_DATABASE_URI = settings.database_url
    DEBUG = settings.debug
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
