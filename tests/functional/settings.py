from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    es_index: dict = {
        'movies':
            [
                'redis_search', 'redis_films', 'limit', 'validation', 'phrase',
                'film', 'all_films', 'films_validation', 'redis_films_id'
            ],
        'genres': ['limit_genre', 'genre_validation', 'redis_genre', 'genre'],
        'persons': ['limit_person', 'person', 'person_validation', 'person_films', 'redis_person']
    }

    es_host: str = Field(default='http://127.0.0.1:9200', alias='TEST_ELASTIC_HOST')
    redis_host: str = Field(default='localhost', alias='TEST_REDIS_HOST')
    redis_port: int = Field(default=6379, env='TEST_REDIS_PORT')
    service_url: str = Field(default='http://127.0.0.1:8000', alias='TEST_SERVICE_URL')

    class Config:
        env_file = '.env.test'


test_settings = TestSettings()
