import random
import pytest
from copy import deepcopy

from tests.functional.settings import test_settings
from tests.functional.conftest import event_loop, es_client, session_client, es_write_data
from tests.functional.testdata.data import PARAMETRES, TEST_DATA
from tests.functional.utils.films_utils import get_es_data, generate_films


@pytest.mark.parametrize('query_data, expected_answer', PARAMETRES['existing_film_id'])
@pytest.mark.asyncio
async def test_get_film_by_id(session_client, es_write_data, query_data: dict, expected_answer: dict):
    film = deepcopy(TEST_DATA)
    film['id'] = test_settings.es_id_field
    data_for_es = get_es_data([film], test_settings.es_index)
    await es_write_data(data_for_es)
    url = test_settings.service_url + f'/api/v1/films/{test_settings.es_id_field}'
    response = await session_client.get(url)
    body = await response.json()
    status = response.status

    assert status == expected_answer['status']
    assert body['uuid'] == expected_answer['answer']


@pytest.mark.parametrize('query_data, expected_answer', PARAMETRES['not_existing_film_id'])
@pytest.mark.asyncio
async def test_get_film_by_not_existing_id(session_client, query_data: dict, expected_answer: dict):
    url = test_settings.service_url + f'/api/v1/films/123e4567-e89b-12d3-a456-426655440000'
    response = await session_client.get(url)
    body = await response.json()
    status = response.status

    assert status == expected_answer['status']
    assert body == expected_answer['answer']


@pytest.mark.asyncio
async def test_get_all_films(session_client, es_write_data):
    count = random.randint(50, 100)
    films = generate_films(count=count)
    data_for_es = get_es_data(films, test_settings.es_index)
    await es_write_data(data_for_es)
    url = test_settings.service_url + f'/api/v1/films/?sort=-imdb_rating&page_size=100&page_number=1'
    response = await session_client.get(url)
    body = await response.json()
    status = response.status

    assert status == 200
    assert len(body) == count
