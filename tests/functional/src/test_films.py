import pytest
from tests.functional.testdata.data import PARAMETERS


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['film_search']
)
@pytest.mark.fixt_data('film')
@pytest.mark.asyncio
async def test_get_film_by_id(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    """
    Тест на поиск фильма по идентификатору. Проверяет также поиск несуществующего фильма.
    :param es_write_data: фикстура для записи данных в ES
    :param make_get_request: фикстура для формирования и отправки запроса
    :param es_data: фикстура генерации данных для последующего добавления в ES
    :param query_data: данные запроса
    :param expected_answer: данные ожидаемого ответа
    :return: None
    """
    # Загружаем данные в ES
    await es_write_data(es_data, 'movies')
    response = await make_get_request('films', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    if 'id' in expected_answer:
        assert response.body['uuid'] == expected_answer['id']
    else:
        assert response.body['detail'] == expected_answer['answer']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    PARAMETERS['all_films']
)
@pytest.mark.fixt_data('all_films')
@pytest.mark.asyncio
async def test_get_all_films(
        es_write_data,
        make_get_request,
        es_data,
        query_data: dict,
        expected_answer: dict
) -> None:
    # Загружаем данные в ES
    await es_write_data(es_data, 'movies')
    response = await make_get_request('films', query_data)
    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']
