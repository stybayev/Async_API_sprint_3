import pytest
from tests.functional.testdata.data import PARAMETERS


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['limit_persons']
)
@pytest.mark.fixt_data('limit_person')
@pytest.mark.asyncio
async def test_person_limit(
        es_write_data,
        make_get_request,
        es_data: list[dict],
        query_data: dict,
        expected_answer: dict
) -> None:
    """
    Проверяем вывод всех персон
    :return:
    """
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('persons', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['search_person']
)
@pytest.mark.fixt_data('peron')
@pytest.mark.asyncio
async def test_search_person(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('persons', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert response.body['name'] == expected_answer['name']
    assert response.body['id'] == expected_answer['id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['person_validation']
)
@pytest.mark.fixt_data('person_validation')
@pytest.mark.asyncio
async def test_validation_person(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # FIX: Тест пока не проходит, потому что можно писать кривые uuid в базу. Надо поправить этот момент
    # Загружаем данные в ES
    await es_write_data(es_data)
    response = await make_get_request('persons', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']
