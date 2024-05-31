from unittest.mock import AsyncMock, MagicMock
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import pytest
from file_api.services.files import FileService


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
