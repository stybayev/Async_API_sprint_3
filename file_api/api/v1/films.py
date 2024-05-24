from fastapi import APIRouter, UploadFile, HTTPException, Depends

from file_api.services.films import MinioStorage, get_film_service

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile, bucket: str,
                      path: str,
                      storage: MinioStorage = Depends(get_film_service)):
    try:
        result = await storage.save(file, bucket, path)
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_name}")
async def get_file(file_name: str):
    # Реализация скачивания файла
    ...
