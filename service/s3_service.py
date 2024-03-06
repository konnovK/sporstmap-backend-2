import os

import boto3
from loguru import logger

from settings import Settings


class S3Service:
    def __init__(self, settings: Settings, bucket: str):
        self.settings = settings

        session = boto3.session.Session()
        self.s3 = session.client(
            service_name='s3',
            endpoint_url=settings.AWS_URL,
            use_ssl=settings.AWS_SSL
        )

        self.bucket = bucket

        self.url_prefix = settings.AWS_URL

    def s3_upload_bytes(self, data: bytes, key: str) -> str | None:
        """Загружает файл в бакет и возвращает ссылку на него, или None, если файл не загрузился"""

        try:
            res = self.s3.put_object(Bucket=self.bucket, Key=key, Body=data)
            logger.debug(res)
            return f'{self.url_prefix}/{self.bucket}/{key}'
        except Exception as e:
            logger.error(e)
            return None

    def s3_delete_elem(self, key: str) -> bool:
        """Удаляет файл из бакета"""

        if self.settings.AWS_ACCESS_KEY_ID is None or self.settings.AWS_SECRET_ACCESS_KEY is None:
            logger.debug(f"[{os.getpid()}] FAILED SETUP S3 SERVICE.")
            logger.debug('AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None')
            return False

        try:
            res = self.s3.delete_object(Bucket=self.bucket, Key=key)
            logger.debug(res)
            return True
        except Exception as e:
            logger.error(e)
            return False
