import os
from functools import lru_cache
from fastapi import UploadFile, Depends
from miniopy_async import Minio
from miniopy_async.helpers import ObjectWriteResult

from file_api.db.minio import get_minio


class MinioStorage:
    def __init__(self, minio: Minio) -> None:
        self.client = minio

    async def save(self, file: UploadFile, bucket: str, path: str) -> ObjectWriteResult:
        # Читаем весь файл для получения его размера
        file_content = await file.read()
        file_size = len(file_content)
        # Возвращаем указатель в начало файла
        await file.seek(0)
        # Загружаем файл в Minio
        result = await self.client.put_object(
            bucket_name=bucket, object_name=path, data=file.file, length=file_size, part_size=10 * 1024 * 1024,
        )
        return result


@lru_cache()
def get_film_service(minio: Minio = Depends(get_minio)) -> MinioStorage:
    return MinioStorage(minio)
