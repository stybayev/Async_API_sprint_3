from copy import deepcopy
from typing import List
import requests
import pytest

from tests.functional.settings import test_settings
from tests.functional.conftest import event_loop, es_add_film, es_client, session_client, make_get_request, \
    es_write_data
from tests.functional.testdata.data import PARAMETRES, TEST_DATA


def get_es_actions(data: List[dict], index: str) -> list[dict]:
    return [{"_index": index, "_source": doc, "_id": doc["id"]} for doc in data]


@pytest.mark.parametrize('query_data, expected_answer', PARAMETRES['existing_film_id'])
@pytest.mark.asyncio
async def test_get_film_by_id(session_client, es_write_data, query_data: dict, expected_answer: dict):
    film = deepcopy(TEST_DATA)
    film['id'] = test_settings.es_id_field
    actions = get_es_actions([film], test_settings.es_index)
    await es_write_data(actions)
    url = test_settings.service_url + f'/api/v1/films/{test_settings.es_id_field}'
    response = await session_client.get(url)
    body = await response.json()
    status = response.status

    assert status == expected_answer['status']
    assert body['uuid'] == expected_answer['answer']


@pytest.mark.parametrize('query_data, expected_answer', PARAMETRES['not_existing_film_id'])
@pytest.mark.asyncio
async def test_get_film_by_not_existing_id(make_get_request, query_data: dict, expected_answer: dict):
    response = await make_get_request('films', query_data)
    body = response.body
    status = response.status

    assert status == expected_answer['status']
    assert body == expected_answer['answer']
