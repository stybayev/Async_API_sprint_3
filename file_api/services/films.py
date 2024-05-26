from functools import lru_cache
from fastapi import UploadFile, Depends
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from file_api.db.db import get_db_session
from file_api.db.minio import get_minio
from file_api.models.files import FileDbModel
from shortuuid import uuid as shortuuid


class FileService:
    def __init__(self, minio: Minio, db_session: AsyncSession) -> None:
        self.client = minio
        self.db_session = db_session

    async def save(self, file: UploadFile, bucket: str, path: str) -> FileDbModel:
        # Получаем размер файла для поля size
        file_content = await file.read()
        file_size = len(file_content)
        await file.seek(0)

        # Определяем значение поля short_name
        short_name = shortuuid()

        # Загружаем файл в Minio
        await self.client.put_object(
            bucket_name=bucket, object_name=path,
            data=file.file, length=file_size,
            part_size=10 * 1024 * 1024,
        )

        # Сохраняем информацию о файле в базу данных
        new_file = FileDbModel(
            path_in_storage=path,
            filename=file.filename,
            short_name=short_name,
            size=file_size,
            file_type=file.content_type,
        )
        self.db_session.add(new_file)
        await self.db_session.commit()
        await self.db_session.refresh(new_file)
        return new_file


@lru_cache()
def get_film_service(minio: Minio = Depends(get_minio),
                     db_session: AsyncSession = Depends(get_db_session)) -> FileService:
    return FileService(minio, db_session)
