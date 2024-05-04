import asyncio
import uuid
import datetime
import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from utils.dc_objects import Response

from settings import test_settings


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(
        hosts=test_settings.es_host,
        verify_certs=False
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='session_client', scope='session')
async def session_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture()
def es_data():
    # Генерируем данные для ES
    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
            {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
        ],
        'writers': [
            {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
            {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
        ],
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat(),
        'film_work_type': 'movie'
    } for _ in range(60)]

    bulk_query: list[dict] = []

    for row in es_data:
        data = {'_index': 'movies', '_id': row['id']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(
            index=test_settings.es_index,
            #**MAPPING_MOVIES
        )

        updated, errors = await async_bulk(client=es_client, actions=data)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(session_client):
    async def inner(type_api, query_data) -> Response:
        url = test_settings.service_url + '/api/v1/films/' + type_api + '/'
        # тут title заменим на query после смены API
        query_data = {'title': query_data[type_api]}
        async with session_client.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        return Response(body, headers, status)
    return inner

