import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from file_api.models.files import FileDbModel
from file_api.services.files import FileService
from file_api.utils.exceptions import NotFoundException


@pytest.fixture
def mock_minio_client():
    client = MagicMock()
    client.put_object = AsyncMock()
    client.get_object = AsyncMock()
    client.get_presigned_url = AsyncMock()
    return client


@pytest.fixture
def mock_db_session():
    session = MagicMock(spec=AsyncSession)
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def file_service(mock_minio_client, mock_db_session):
    return FileService(mock_minio_client, mock_db_session)


@pytest.fixture
def test_file():
    file = MagicMock(spec=UploadFile)
    file.filename = "test.txt"
    file.content_type = "text/plain"
    file.read = AsyncMock(return_value=b"test content")
    file.seek = AsyncMock()
    file.file = MagicMock()  # Добавление атрибута `file`
    return file

@pytest.mark.asyncio
async def test_save_file(file_service, test_file):
    path = "test/path"
    file_record = await file_service.save(test_file, path)

    assert file_record.filename == test_file.filename
    assert file_record.file_type == test_file.content_type
    assert file_record.size == len(b"test content")
    assert file_record.path_in_storage == path
    file_service.db_session.add.assert_called_once()
    file_service.db_session.commit.assert_called_once()
    file_service.db_session.refresh.assert_called_once()