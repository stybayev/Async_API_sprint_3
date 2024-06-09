import logging
import requests
from uuid import uuid4
from django.core.files.storage import Storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible
from django.core.exceptions import SuspiciousOperation

from config.settings import FILE_SERVICE_URL


@deconstructible
class CustomStorage(Storage):
    def _save(self, name, content: InMemoryUploadedFile):
        unique_name = f"{uuid4()}/{name}"  # Генерация уникального имени с использованием UUID
        try:
            response = requests.post(
                f"{FILE_SERVICE_URL}/upload/?path={unique_name}",
                files={"file": (content.name, content, content.content_type)},
            )
            response.raise_for_status()  # Проверяем успешность запроса

            response_data = response.json()
            logging.info(response_data)

            short_name = response_data.get("short_name")
            if not short_name:
                raise SuspiciousOperation("File upload failed, short_name not found in response")

            return short_name
        except requests.RequestException as e:
            logging.error(f"Error uploading file: {e}")
            raise SuspiciousOperation("File upload failed due to a request error")

    def url(self, name):
        return f"{FILE_SERVICE_URL}/download/{name}"

    def exists(self, name):
        # Если у вас есть возможность проверять существование файла на сервере, добавьте эту логику здесь
        return False
