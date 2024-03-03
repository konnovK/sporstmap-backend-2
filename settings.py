import os

from loguru import logger

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    API_HOST: str | None = None
    API_PORT: int = 8080
    API_DB_URL: str
    API_DB_USE_SSL: bool = False

    API_SUPERUSER_EMAIL: str | None = None
    API_SUPERUSER_PASSWORD: str | int | None = None

    YANDEX_GEOCODER_API_KEY: str | None = None

    AWS_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    API_DEBUG: bool = False

    SMTP_HOST: str = 'smtp.yandex.ru'
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    @staticmethod
    def new():
        try:
            settings = Settings(_env_file='.env')
            settings.API_SUPERUSER_PASSWORD = str(settings.API_SUPERUSER_PASSWORD)
            os.environ.update({
                "AWS_ACCESS_KEY_ID": settings.AWS_ACCESS_KEY_ID,
                "AWS_SECRET_ACCESS_KEY": settings.AWS_SECRET_ACCESS_KEY
            })
            return settings
        except ValidationError as err:
            logger.critical(err)
            exit(1)
