from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import ORJSONResponse
from file_api.api.v1 import films
from file_api.core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    # lifespan=lifespan
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
