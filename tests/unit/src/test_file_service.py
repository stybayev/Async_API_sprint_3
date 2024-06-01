import pytest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.future import select

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
