from unittest.mock import AsyncMock

import pytest
from starlette.responses import StreamingResponse

from file_api.models.files import FileDbModel
from file_api.utils.exceptions import NotFoundException


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
