from fastapi import APIRouter, UploadFile, HTTPException, Depends

from file_api.schemas.files import FileResponse
from file_api.services.files import FileService, get_film_service

router = APIRouter()


@router.post("/upload/", response_model=FileResponse)
async def upload_file(file: UploadFile,
                      bucket: str,
                      path: str,
                      service: FileService = Depends(get_film_service)):
    """
    ## Загрузка файла

    Этот эндпоинт позволяет загрузить файл в указанный S3 бакет и путь. Файл сохраняется в хранилище MinIO, а метаданные файла сохраняются в базе данных PostgreSQL.

    ### Параметры:
    - **file**: Загружаемый файл.
    - **bucket**: Имя S3 бакета, в который будет сохранен файл, по дефолту - movies.
    - **path**: Путь внутри бакета, по которому будет сохранен файл.

    ### Возвращает:
      - `id`: Уникальный идентификатор файла.
      - `path_in_storage`: Полный путь к файлу в хранилище.
      - `filename`: Оригинальное имя файла.
      - `size`: Размер файла в байтах.
      - `file_type`: MIME-тип файла.
      - `short_name`: Короткое, уникальное имя файла.
      - `created_at`: Временная метка создания файла.
    """
    try:
        file_record = await service.save(file, bucket, path)
        return FileResponse(
            id=file_record.id,
            path_in_storage=file_record.path_in_storage,
            filename=file_record.filename,
            size=file_record.size,
            file_type=file_record.file_type,
            short_name=file_record.short_name,
            created_at=file_record.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_name}")
async def get_file(file_name: str):
    # Реализация скачивания файла
    ...
