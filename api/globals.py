import yandexcloud
from loguru import logger

from api.context import AppContext
from api.utils.logger import YandexHandler
from settings import Settings

settings = Settings.new()

app_context = AppContext(settings)

__all__ = [
    settings,
    app_context
]
