from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env='ELASTIC_HOST')
    es_index: str = Field(default='movies')
    es_id_field: str = Field(default='ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd')
    redis_host: str = Field(env='REDIS_HOST')
    service_url: str = Field(default='http://0.0.0.0:8000', env='SERVICE_URL')


test_settings = TestSettings()
