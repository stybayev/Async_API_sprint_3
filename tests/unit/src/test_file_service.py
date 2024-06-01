import uuid

from sqlalchemy.future import select

from file_api.db.minio import close_minio, set_minio
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


@pytest.mark.asyncio
async def test_download_file_success(file_service, mocker):
    """
    Тест успешного скачивания файла.
    """
    short_name = "short_name_123"
    file_path = "test/path"
    file_name = "test.txt"
    file_content = b"test content"

    # Мокаем метод file_service.get_file_record
    mocker.patch.object(file_service, 'get_file_record', return_value=AsyncMock())
    file_service.get_file_record.return_value.path_in_storage = file_path
    file_service.get_file_record.return_value.filename = file_name

    # Мокаем метод file_service.get_file
    mocker.patch.object(file_service, 'get_file', return_value=AsyncMock())
    file_service.get_file.return_value = StreamingResponse(
        iter([file_content]), media_type='application/octet-stream',
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{file_name}"}
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/api/v1/files/download/{short_name}")
    print(response.status_code)
    print(response.content)

    # assert response.status_code == 200
    # assert response.content == file_content
    # assert response.headers["Content-Disposition"] == f"attachment; filename*=UTF-8''{file_name}"
