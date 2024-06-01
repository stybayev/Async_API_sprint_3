import uuid

from sqlalchemy.future import select

from file_api.db.db import get_db_session
from file_api.db.minio import close_minio, set_minio, get_minio
from file_api.models.files import FileDbModel
from unittest.mock import AsyncMock, MagicMock
from aiohttp import ClientResponse, StreamReader
from starlette.responses import StreamingResponse
from file_api.utils.exceptions import NotFoundException
from fastapi import status
from httpx import AsyncClient
import pytest

from file_api.main import app
from file_api.schemas.files import FileResponse


@pytest.mark.asyncio
async def test_save_file(file_service, test_file):
    """
    Тест сохранения файла
    """
    path = "test/path"
    file_record = await file_service.save(test_file, path)

    assert file_record.filename == test_file.filename
    assert file_record.file_type == test_file.content_type
    assert file_record.size == len(b"test content")
    assert file_record.path_in_storage == path
    file_service.db_session.add.assert_called_once()
    file_service.db_session.commit.assert_called_once()
    file_service.db_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_file_record_success(file_service, mock_db_session):
    """
    Тест успешного получения записи файла по короткому имени.
    """
    short_name = "short_name_123"
    mock_file_record = FileDbModel(
        path_in_storage="test/path",
        filename="test.txt",
        short_name=short_name,
        size=123,
        file_type="text/plain",
    )

    # Настраиваем mock на возврат записи файла
    mock_db_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=mock_file_record)

    # Сравнение вызова get_file_record
    file_record = await file_service.get_file_record(short_name)
    assert file_record == mock_file_record

    # Проверка вызова метода execute
    query = select(FileDbModel).where(FileDbModel.short_name == short_name)
    mock_db_session.execute.assert_called_once()
    args, _ = mock_db_session.execute.call_args
    assert str(args[0]) == str(query)


@pytest.mark.asyncio
async def test_get_file_record_not_found(file_service, mock_db_session):
    """
    Тест ситуации, когда запись файла не найдена по короткому имени.
    """
    short_name = "short_name_123"

    mock_db_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=None)

    with pytest.raises(NotFoundException) as exc_info:
        await file_service.get_file_record(short_name)

    assert exc_info.value.detail == 'File not found'


@pytest.mark.asyncio
async def test_get_file(file_service, mock_minio_client):
    """
    Тест успешного получения файла из Minio.
    """
    path = "test/path"
    filename = "test.txt"
    content = b"test content"

    # Создаем mock ответа Minio get_object
    mock_response = MagicMock(ClientResponse)
    mock_response.content = MagicMock(StreamReader)
    mock_response.content.iter_chunked = AsyncMock(return_value=[content])
    mock_minio_client.get_object.return_value = mock_response

    response = await file_service.get_file(path, filename)
    assert isinstance(response, StreamingResponse)


@pytest.mark.asyncio
async def test_get_presigned_url(file_service, mock_db_session, mock_minio_client):
    """
    Тест успешного получения подписанной ссылки.
    """
    short_name = "short_name_123"

    # Настраиваем mock на возврат записи файла
    mock_presigned_url = "http://presigned.url"
    mock_minio_client.get_presigned_url.return_value = mock_presigned_url

    # Сравнение вызова get_presigned_url
    presigned_url = await file_service.get_presigned_url(short_name)
    assert presigned_url == mock_presigned_url


@pytest.mark.anyio
async def test_ping():
    async with AsyncClient(app=app, base_url='http://localhost/api/v1/files/') as client:
        response = await client.get('/')
    # print(response.content)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_download_file_success(mock_db_session, mock_minio_client):
    """
    Тест успешного скачивания файла.
    """
    short_name = "short_name_123"
    path_in_storage = "test/path"
    filename = "test.txt"
    content = b"test content"

    # Настраиваем mock на возврат записи файла
    mock_file_record = FileDbModel(
        path_in_storage=path_in_storage,
        filename=filename,
        short_name=short_name,
        size=123,
        file_type="text/plain"
    )

    # Обратите внимание на await для возвращения mock записи
    mock_db_session.execute.return_value.scalar_one_or_none = MagicMock(return_value=mock_file_record)

    # Создаем mock ответа Minio get_object
    async def mock_iter_chunked(chunk_size):
        yield content

    mock_response = MagicMock(ClientResponse)
    mock_stream_reader = MagicMock(StreamReader)
    mock_stream_reader.iter_chunked = mock_iter_chunked
    mock_response.content = mock_stream_reader
    mock_minio_client.get_object.return_value = mock_response

    # Переопределяем зависимости в FastAPI
    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    app.dependency_overrides[get_minio] = lambda: mock_minio_client

    async with AsyncClient(app=app, base_url="http://localhost/api/v1/files") as client:
        response = await client.get(f"/download/{short_name}")

    response_content = await response.aread()

    assert response.status_code == status.HTTP_200_OK
    assert response_content == content
    assert response.headers["content-disposition"] == f"attachment; filename*=UTF-8''{filename}"

    # Сбрасываем переопределения
    app.dependency_overrides = {}
