import pytest
from conftest import (es_write_data, event_loop, es_data,
                      make_get_request, es_client, session_client)
from testdata.data import PARAMETERS


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['limit_genres']
)
@pytest.mark.fixt_data('limit_genre')
@pytest.mark.asyncio
async def test_genre_limit(
        es_write_data,
        make_get_request,
        es_data: list[dict],
        query_data: dict,
        expected_answer: dict
) -> None:
    """
    Проверяем вывод всех жанров
    :return:
    """
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('genres', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['search_genre']
)
@pytest.mark.fixt_data('genre')
@pytest.mark.asyncio
async def test_search_genre(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('genres', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert response.body['name'] == expected_answer['name']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['genre_validation']
)
@pytest.mark.fixt_data('genre_validation')
@pytest.mark.asyncio
async def test_search_genre(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('genres', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']
