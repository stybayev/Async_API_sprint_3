from contextlib import asynccontextmanager
from miniopy_async import Minio
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from file_api.api.v1 import films
from file_api.core.config import settings
from file_api.db.minio import get_minio, client


@asynccontextmanager
async def lifespan(app: FastAPI):
    minio_client = get_minio()
    yield
    await minio_client.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
