import pytest
import io
import datetime
from unittest.mock import patch, Mock, MagicMock
from file_api.models.files import FileDbModel
from fastapi import status, UploadFile, File
from httpx import AsyncClient
from file_api.api.v1.files import upload_file
from miniopy_async import Minio
from file_api.services.files import FileService
from file_api.schemas.files import FileResponse
# from file_api.core.config import settings
from file_api.main import app
from file_api.services.files import FileService


class FakeFileService:
    @staticmethod
    def save() -> dict:
        return {
            'path_in_storage': 'test_movies',
            'filename': 'downloaded_file.mp4',
            'size': 111,
            'file_type': 'video/mp4',
            'short_name': 'RXMtYTzn3vXRufYvYBRvUH',
            'id': '5be28c6b-163c-4524-8f2c-7d8c429cd123',
            'created_at': datetime.datetime(2023, 1, 1)
        }


@pytest.mark.anyio
async def test_upload_file(mocker):
    mocker.patch('file_api.api.v1.files.get_file_service', return_value=FakeFileService)
    video = {"file": open("testdata/downloaded_file.mp4", 'rb')}
    url = 'http://localhost:8081/api/v1/files'
    async with AsyncClient(app=app, base_url=url) as client:
        response = await client.post(url="/upload/", files=video, data={'path': 'test_movies'})


    # сформировали видео для отправки пост-запросом

    #
    # assert response.status_code == status.HTTP_200_OK
    # print('JSON: ')
    # print(response.json())
