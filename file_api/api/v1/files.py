from fastapi import APIRouter, UploadFile, HTTPException, Depends

from file_api.schemas.files import FileResponse
from file_api.services.films import FileService, get_film_service

router = APIRouter()


@router.post("/upload/", response_model=FileResponse)
async def upload_file(file: UploadFile, bucket: str, path: str,
                      service: FileService = Depends(get_film_service)):
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
