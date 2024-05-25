from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile):
    ...


@router.get("/download/{file_name}")
async def get_file(file_name: str):
    ...
