# file_api/db/minio.py
from miniopy_async import Minio
from file_api.core.config import settings

client: Minio | None = None


def get_minio() -> Minio:
    global client
    if client is None:
        client = Minio(
            endpoint=settings.minio_host,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False,
        )
    return client
