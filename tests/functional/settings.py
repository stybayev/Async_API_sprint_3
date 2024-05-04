import os

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class TestSettings(BaseSettings):
    es_host: str = Field('http://127.0.0.1:9200', env=os.getenv('ELASTICSEARCH_HOST'))
    es_index: str = Field(default='movies')
    es_id_field: str = Field(default='ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd')
    es_index_mapping: dict = {
        'actors': {
            'properties': {
                'id': {
                    'type': 'text',
                    'fields': {
                        'keyword': {
                            'type': 'keyword'
                        }
                    }
                },
                'name': {
                    'type': 'text',
                    'fields': {
                        'keyword': {
                            'type': 'keyword'
                        }
                    }
                }
            }
        },
        'actors_names': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'created_at': {
            'type': 'date'
        },
        'description': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'director': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'film_work_type': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'genre': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'id': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'imdb_rating': {
            'type': 'float'
        },
        'title': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        },
        'updated_at': {
            'type': 'date'
        },
        'writers': {
            'properties': {
                'id': {
                    'type': 'text',
                    'fields': {
                        'keyword': {
                            'type': 'keyword'
                        }
                    }
                },
                'name': {
                    'type': 'text',
                    'fields': {
                        'keyword': {
                            'type': 'keyword'
                        }
                    }
                }
            }
        },
        'writers_names': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword'
                }
            }
        }

    }
    redis_host: str = Field(env=os.getenv('REDIS_HOST'))
    service_url: str = Field(default='http://127.0.0.1:81', env=os.getenv('SERVICE_URL'))


test_settings = TestSettings()
