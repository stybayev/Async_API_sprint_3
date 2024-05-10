import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.test')


class TestSettings(BaseSettings):
    es_host: str = Field(default=os.getenv('TEST_ELASTIC_HOST', 'http://127.0.0.1:9200'))
    es_index: dict = {
        'movies':
            [
                'redis_search', 'redis_films','limit', 'validation', 'phrase',
                'film', 'all_films', 'films_validation', 'redis_films_id'
            ],
        'genres': ['limit_genre', 'genre_validation', 'redis_genre', 'genre'],
        'persons': ['limit_person', 'person', 'person_validation', 'person_films', 'redis_person']
    }
    redis_host: str = Field(default=os.getenv('TEST_REDIS_HOST', 'localhost'))
    redis_port: int = Field(default=os.getenv('TEST_REDIS_PORT', 6379))
    service_url: str = Field(default=os.getenv('TEST_SERVICE_URL', 'http://127.0.0.1:8000'))


test_settings = TestSettings()
