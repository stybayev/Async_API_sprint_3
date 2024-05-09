import os

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

if os.path.exists('/.dockerenv'):
    load_dotenv()
else:
    load_dotenv(dotenv_path='.env.local')


class TestSettings(BaseSettings):
    es_host: str = Field('http://elasticsearch-test:9200', env='ELASTIC_HOST')
    es_index: str = Field(default='movies')
    redis_host: str = Field(default=os.getenv('REDIS_HOST', 'localhost'))
    service_url: str = Field(default='http://fastapi:8080', env='SERVICE_URL')
    # es_mapping = {
    #     "movies": {
    #         "mappings": {
    #             "dynamic": "strict",
    #             "properties": {
    #                 "actors": {
    #                     "type": "nested",
    #                     "dynamic": "strict",
    #                     "properties": {
    #                         "id": {
    #                             "type": "keyword"
    #                         },
    #                         "name": {
    #                             "type": "text",
    #                             "analyzer": "ru_en"
    #                         }
    #                     }
    #                 },
    #                 "actors_names": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     },
    #                     "analyzer": "ru_en"
    #                 },
    #                 "description": {
    #                     "type": "text",
    #                     "analyzer": "ru_en"
    #                 },
    #                 "director": {
    #                     "dynamic": "strict",
    #                     "properties": {
    #                         "id": {
    #                             "type": "keyword"
    #                         },
    #                         "name": {
    #                             "type": "text",
    #                             "fields": {
    #                                 "raw": {
    #                                     "type": "keyword"
    #                                 }
    #                             },
    #                             "analyzer": "ru_en"
    #                         }
    #                     }
    #                 },
    #                 "genre": {
    #                     "type": "keyword"
    #                 },
    #                 "id": {
    #                     "type": "keyword"
    #                 },
    #                 "imdb_rating": {
    #                     "type": "float"
    #                 },
    #                 "title": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     },
    #                     "analyzer": "ru_en"
    #                 },
    #                 "writers": {
    #                     "type": "nested",
    #                     "dynamic": "strict",
    #                     "properties": {
    #                         "id": {
    #                             "type": "keyword"
    #                         },
    #                         "name": {
    #                             "type": "text",
    #                             "analyzer": "ru_en"
    #                         }
    #                     }
    #                 },
    #                 "writers_names": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     },
    #                     "analyzer": "ru_en"
    #                 }
    #             }
    #         }
    #     },
    #     "persons": {
    #         "mappings": {
    #             "dynamic": "strict",
    #             "properties": {
    #                 "full_name": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     }
    #                 },
    #                 "id": {
    #                     "type": "keyword"
    #                 }
    #             }
    #         }
    #     },
    #     "genres": {
    #         "mappings": {
    #             "dynamic": "strict",
    #             "properties": {
    #                 "description": {
    #                     "type": "text"
    #                 },
    #                 "id": {
    #                     "type": "keyword"
    #                 },
    #                 "name": {
    #                     "type": "text",
    #                     "fields": {
    #                         "raw": {
    #                             "type": "keyword"
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # }

test_settings = TestSettings()
