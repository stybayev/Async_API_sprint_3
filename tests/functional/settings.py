import os

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

if os.path.exists('/.dockerenv'):
    load_dotenv()
else:
    load_dotenv(dotenv_path='.env.local')


class TestSettings(BaseSettings):
    es_host: str | None = None
    es_index: str | None = None
    redis_host: str | None = None

    if os.path.exists('/.dockerenv'):
        # Docker
        es_host: str = Field('http://elasticsearch:9200')
        es_index: str = Field(default='movies')
        redis_host: str = Field('redis')
        service_url: str = Field(default='http://app:8000')
    else:
        # Local
        es_host: str = Field('http://127.0.0.1:9200')
        es_index: str = Field(default='movies')
        redis_host: str = Field('localhost')
        service_url: str = Field('http://127.0.0.1:8000')


test_settings = TestSettings()
