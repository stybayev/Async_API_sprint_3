import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from file_api.services.files import FileService
from file_api.models.files import FileDbModel
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
    return file

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

async def test_get_file_record(file_service):
    short_name = "test_short_name"
    expected_record = FileDbModel(
        path_in_storage="test/path",
        filename="test.txt",
        short_name=short_name,
        size=100,
        file_type="text/plain"
    )

    file_service.db_session.execute.return_value.scalar_one_or_none = AsyncMock(return_value=expected_record)
    file_record = await file_service.get_file_record(short_name)
    assert file_record == expected_record

async def test_get_file_record_not_found(file_service):
    short_name = "nonexistent_short_name"
    file_service.db_session.execute.return_value.scalar_one_or_none = AsyncMock(return_value=None)

    with pytest.raises(NotFoundException):
        await file_service.get_file_record(short_name)
