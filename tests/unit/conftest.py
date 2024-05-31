import pytest
from unittest.mock import AsyncMock
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from file_api.services.files import FileService


@pytest.fixture
def mock_minio_client(mocker):
    client = mocker.Mock()
    client.put_object = AsyncMock()
    client.get_object = AsyncMock()
    client.get_presigned_url = AsyncMock()
    return client


@pytest.fixture
def mock_db_session(mocker):
    session = mocker.Mock(spec=AsyncSession)
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def file_service(mock_minio_client, mock_db_session):
    return FileService(mock_minio_client, mock_db_session)


@pytest.fixture
def test_file(mocker):
    file = mocker.Mock(spec=UploadFile)
    file.filename = "test.txt"
    file.content_type = "text/plain"
    file.read = AsyncMock(return_value=b"test content")
    file.seek = AsyncMock()
    file.file = mocker.Mock()  # Добавление атрибута `file`
    return file
