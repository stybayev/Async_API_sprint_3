import pytest
from tests.functional.testdata.data import PARAMETERS
from tests.functional.utils.films_utils import get_es_data
from tests.functional.testdata.data import TEST_DATA_PERSON


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
    await es_write_data(es_data, 'persons')
    response = await make_get_request('persons', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['search_person']
)
@pytest.mark.fixt_data('person')
@pytest.mark.asyncio
async def test_search_person(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data, 'persons')
    response = await make_get_request('persons', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert response.body == expected_answer['answer']


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
    await es_write_data(es_data, 'persons')
    response = await make_get_request('persons', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['person_films']
)
@pytest.mark.fixt_data('person_films')
@pytest.mark.asyncio
async def test_films_by_person(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    await es_write_data(es_data, 'movies')
    data = get_es_data([TEST_DATA_PERSON], 'persons')
    await es_write_data(data, 'persons')

