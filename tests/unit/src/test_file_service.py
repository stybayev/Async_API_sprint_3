import pytest
from unittest.mock import AsyncMock
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
async def test_get_file_record_found(file_service, mock_db_session):
    """
    Тест успешного получения записи о файле
    """
    # Создаем фейковую запись о файле
    file_record = FileDbModel(
        path_in_storage="test/path",
        filename="test.txt",
        short_name="short_name",
        size=123,
        file_type="text/plain",
    )

    # Настраиваем возвращаемое значение для execute
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = file_record
    mock_db_session.execute.return_value = mock_result

    # Вызываем метод
    result = await file_service.get_file_record("short_name")

    # Проверяем результат
    assert result == file_record
    mock_db_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_file_record_not_found(file_service, mock_db_session):
    """
    Тест получения записи о файле, когда файл не найден
    """
    # Настраиваем возвращаемое значение для execute
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result

    # Вызываем метод и проверяем, что возникает исключение NotFoundException
    with pytest.raises(NotFoundException):
        await file_service.get_file_record("non_existent_short_name")

    mock_db_session.execute.assert_called_once()
