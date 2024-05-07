import pytest
from conftest import (es_write_data, event_loop, es_data,
                                       make_get_request, es_client, session_client)
from testdata.data import PARAMETRES


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETRES['limit']
)
@pytest.mark.fixt_data('limit')
@pytest.mark.asyncio
async def test_search_limit(
        es_write_data,
        make_get_request,
        es_data: list[dict],
        query_data: dict,
        expected_answer: dict
) -> None:
    """
    Проверка, что поиск по названию фильма
    возвращает только первые 10 результатов
    :return:
    """
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('films/search', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETRES['validation']
)
@pytest.mark.fixt_data('validation')
@pytest.mark.asyncio
async def test_search_validation(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('films/search', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETRES['phrase']
)
@pytest.mark.fixt_data('phrase')
@pytest.mark.asyncio
async def test_search_phrase(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('films/search', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']
