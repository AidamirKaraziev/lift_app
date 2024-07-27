import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, root_validator, validator


def get_url():
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")  # Используйте "localhost" для локального тестирования
    port = os.getenv("DB_PORT", "5435")
    db_name = os.getenv("DB_NAME", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TOKEN_CLAIMS_EXTRA_FIELDS = ["exp", "nbf", "iat", "jti"]
    TOKEN_CHECKS = ["nbf"]

    SERVER_NAME: str = "default_server_name"  # Установите значение по умолчанию
    SERVER_HOST: AnyHttpUrl = "http://localhost"  # Установите значение по умолчанию
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "ELS 🔥"  # Установите значение по умолчанию
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is None or len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str = "localhost"  # Установите значение по умолчанию
    POSTGRES_USER: str = "user"  # Установите значение по умолчанию
    POSTGRES_PASSWORD: str = "password"  # Установите значение по умолчанию
    POSTGRES_DB: str = "database"  # Установите значение по умолчанию
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = get_url()

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @root_validator(pre=True)
    def set_email_from_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if 'EMAILS_FROM_NAME' not in values or values['EMAILS_FROM_NAME'] is None:
            values['EMAILS_FROM_NAME'] = values.get('PROJECT_NAME', 'ELS')
        return values

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "users@example.com"  # Установите значение по умолчанию
    FIRST_SUPERUSER_PASSWORD: str = "supersecretpassword"  # Установите значение по умолчанию
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
