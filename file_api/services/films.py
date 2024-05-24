import os
from fastapi import UploadFile
from miniopy_async import Minio
from miniopy_async.helpers import ObjectWriteResult


class MinioStorage:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv('MINIO_HOST'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=False,
        )

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
