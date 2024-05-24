from fastapi import APIRouter, UploadFile, HTTPException

from file_api.services.films import MinioStorage

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile, bucket: str, path: str):
    storage = MinioStorage()
    try:
        result = await storage.save(file, bucket, path)
        return {"result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_name}")
async def get_file(file_name: str):
    # Реализация скачивания файла
    ...
