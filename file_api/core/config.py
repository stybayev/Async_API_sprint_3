import os
from logging import config as logging_config
from pydantic import BaseSettings, Field
from app.core.logger import LOGGING


class Settings(BaseSettings):
    # App
    project_name: str = Field(default="File API", env="File API")
    uvicorn_host: str = Field(default="0.0.0.0", env="FILE_API_UVICORN_HOST")
    uvicorn_port: int = Field(default=8001, env="FILE_API_UVICORN_PORT")

    # Redis
    redis_host: str = Field(default="0.0.0.0", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")

    # Elastic
    elastic_host: str = Field(default="0.0.0.0", env="ELASTIC_HOST")
    elastic_port: int = Field(default=9200, env="ELASTIC_PORT")

    # MinIO
    minio_host: str = Field(default="0.0.0.0", env="MINIO_HOST")
    minio_port: int = Field(default=9000, env="MINIO_PORT")
    minio_access_key: str = Field(default="minioadmin", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", env="MINIO_SECRET_KEY")

    class Config:
        env_file = ".env"


# Создаем экземпляр класса Settings для хранения настроек
settings = Settings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
