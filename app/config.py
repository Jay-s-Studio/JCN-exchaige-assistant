"""
Configuration
"""
import json
import os
from distutils.util import strtobool
from pathlib import Path, PosixPath
from typing import List, Optional, Any, Type, Tuple

from dotenv import load_dotenv
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, EnvSettingsSource, PydanticBaseSettingsSource

from app.libs.consts.enums import BotType

load_dotenv()


class MyCustomSource(EnvSettingsSource):

    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool
    ) -> Any:
        if field.annotation is List[str]:
            return [v for v in value.split(',')]
        return value


class Configuration(BaseSettings):
    """
    Configuration
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)

    # [App Base]
    APP_NAME: str = "jcn_exchaige_assistant"
    ENV: str = os.getenv(key="ENV", default="dev").lower()
    DEBUG: bool = os.getenv(key="DEBUG", default=False)
    IS_PROD: bool = ENV == "prod"
    IS_DEV: bool = ENV not in ["prod", "stg"]
    APP_FQDN: str = os.getenv(key="APP_FQDN", default="localhost")
    BASE_URL: str = f"https://{APP_FQDN}"

    # [Special]
    ALLOWED_PATHS: List[str] = os.getenv(key="ALLOWED_PATHS", default="/api/healthcheck").split(",")

    # [FastAPI]
    HOST: str = os.getenv(key="HOST", default="127.0.0.1")
    PORT: int = os.getenv(key="PORT", default=8000)

    # [CORS]
    CORS_ALLOWED_ORIGINS: List[str] = os.getenv(key="CORS_ALLOWED_ORIGINS", default="*").split(",")
    CORS_ALLOW_ORIGINS_REGEX: Optional[str] = os.getenv(key="CORS_ALLOW_ORIGINS_REGEX")

    # [JWT]
    JWT_SECRET: str = os.getenv(key="JWT_SECRET")

    # [Redis]
    REDIS_URL: str = os.getenv(key="REDIS_URL", default="redis://localhost:6379")

    # [PostgreSQL]
    DATABASE_HOST: str = os.getenv(key="DATABASE_HOST", default="localhost")
    DATABASE_USER: str = os.getenv(key="DATABASE_USER", default="postgres")
    DATABASE_PASSWORD: str = os.getenv(key="DATABASE_PASSWORD", default="")
    DATABASE_PORT: str = os.getenv(key="DATABASE_PORT", default="5432")
    DATABASE_NAME: str = os.getenv(key="DATABASE_NAME", default="postgres")
    DATABASE_SCHEMA: Optional[str] = os.getenv(key="DATABASE_SCHEMA")
    DATABASE_APPLICATION_NAME: str = APP_NAME

    # [Database]
    DATABASE_POOL: bool = strtobool(os.getenv("DATABASE_POOL", "true"))
    SQL_ECHO: bool = strtobool(os.getenv("SQL_ECHO", "false"))
    SQLALCHEMY_DATABASE_URI: str = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                                   f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    ASYNC_DATABASE_URL: str = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@' \
                              f'{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

    # [Telegram]
    TELEGRAM_BOT_USERNAME: str = os.getenv(key="TELEGRAM_BOT_USERNAME")
    TELEGRAM_BOT_TOKEN: str = os.getenv(key="TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_TYPE: BotType = BotType.CUSTOMER

    # [Gina]
    GINA_URL: str = os.getenv(key="GINA_URL")
    GINA_API_KEY: str = os.getenv(key="GINA_API_KEY")

    # [Sentry]
    SENTRY_URL: str = os.getenv(key="SENTRY_URL")

    # [Google Cloud]
    google_certificate_path: PosixPath = Path("env/google_certificate.json") if IS_DEV else Path("/etc/secrets/google_certificate.json")
    GOOGLE_FIREBASE_CERTIFICATE: dict = {
        "type": "service_account",
        "project_id": "jcn-exchaige-assistant-dev",
        "private_key_id": "e3e23a0311df7829f12d60d9d7c486aae28d3923",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcHaH8Ds+EGELH\nkK1bbJbCgqXVnTzlrT5mvCs8NCr/4Nbs7UnZq+mfwv34tzE0D9n6btFCMMJbqBAi\nWW2WDZSxqYLBpVrpXl7Ki/LKA8NTHYuXW8DFB+VFQWL+INNxtQhnvY8qfl8aPjf9\nDBN+Ic61B5SnxPJVwso1Fyvd/Ic0qtWnwDQS6lVQMXAQiyfN5RP/NEthcnJrR+zB\n0be5+vVGzWPDO/vjF3Epd9Fndfe+ojvWAosFrumCYC5HJ+PsgC7IjUIOz63ygtyR\njOsMeiJbROlQA4ZulL1xdSDiLALaClT7XyF7tX6ENuw7T6W/xvqRjLcZiS1/Ib5d\nnrrwuf+fAgMBAAECggEAEcZ1+SMekaXJhLt+YZh9mewSQb5Dfss4/a2TJqmx86yA\nDD4AWJ5wXVZwYG9LVOgxI4iWnvi6SIFcROz1w04MjiYE01OmhEfQdzN0E3hWNxJ4\nIGW8DzMU8cu+H71RFfNM37L/qBD3dx96dH95gLUMuiQA0xFjnkwthdn7jq0AIAje\nADUYdH8mW12HPJqYVOGmrPdMthUSL9iMatf/g1K1023U0iKHJOquE04xr4/Ukol2\nU/0uHcxAZXq5AU28fW6NwYvTT8F6nzYQZyyhuvwhUE+bMEbXjOr3vYdjMOBdvWKd\nCuULdhfTYKesjhJ8aADDaGb7Hd9z4MKP+hrc0iRNMQKBgQDJTIeCpuxtZIJUxACy\nruAIgPuZGZ7cLtQnHePXYwffD5mn8B4q0y9z9KqzmKloMEOVmitVoa301IVxOICU\nR9/exXWnlOvYYYW3u7wiYG5ilBJFyZJl/eNRzKffK9W/CqU58VI46ltA+JZvE3rA\nAXrVcSOO4if2mycAFifL48D6cwKBgQDGiekCVQUDNiJtOE4umoasKqZr+NvhRMxG\nhNUpti22bN7H1VWf9A4JNtm1HFmO/p8d/AvVBcid5CiZYHwo547YAJFdSVo/5RYh\n+sNff9zxpUVRrBwwKT9t9ajMPEmM0wT2WPQx8jEXCUrRFGDJHUnDhF5VISERjpuv\n6nagqJ6/JQKBgFiIqDD2aZXTVt8hNY1hDHexAvdbJVuB3R03MDZS/+tDWTlbimkb\naQt+2HUU960zTQZHQDfxXCkKL4aUazjMQ9Ie1phWD0Sj38Pndd9IukPxC/hVp2Xk\nPE6FzG+DQAc+D11knd0adfglXUSNNLet7vBhSlpVbW4w3v5SwD4UdZOxAoGBAIpL\nuG5ycJprFBIGfZdC9npo/yII6IkDVlPs5Vs31qHTNl/2v7060KgkeAQLamsL/CRz\n1H4fmD47lvg32GTZ34ug4aEcnmwRlJg4x+z28R22JRIeFEiMAu4CiAE0IXuh5jv/\nfKJp9T35sA7x5fVRnHc/9kHQYOuM7e/dH6MLsgCtAoGAWTwQqhYwoxF3PZBu39uz\nqQMv+AJdaMBKVtZQjX6sSRQoN+S7cpoEd5ojDuX+PLitW/tUWNfUGm2bpjodJ7Jw\n5wFdLTIezpAwtsys7oZynYNhc3w07dOVmx/8iUcOSKsDWjGWUryxNEfJO4crgdPY\nUOEmWHuQn5s6XXbxutoebq0=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-gniqy@jcn-exchaige-assistant-dev.iam.gserviceaccount.com",
        "client_id": "107860582747874830013",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gniqy%40jcn-exchaige-assistant-dev.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }



settings: Configuration = Configuration()
