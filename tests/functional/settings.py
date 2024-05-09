import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.test')

class TestSettings(BaseSettings):
    es_host: str = Field(default=os.getenv('TEST_ELASTIC_HOST', 'http://127.0.0.1:9200'))
    es_index: str = Field(default='movies')
    redis_host: str = Field(default=os.getenv('TEST_REDIS_HOST', 'localhost'))
    service_url: str = Field(default=os.getenv('TEST_SERVICE_URL', 'http://127.0.0.1:8000'))

test_settings = TestSettings()
