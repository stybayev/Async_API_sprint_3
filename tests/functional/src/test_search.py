import pytest
import time
from conftest import (es_write_data, event_loop, es_data,
                      make_get_request, es_client, session_client)

from settings import test_settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search': 'The Star'},
            {'status': 200, 'length': 40}
        ),
        (
            {'search': 'Marched Potato'},
            {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(
        es_write_data,
        make_get_request,
        es_data: list[dict],
        query_data: dict,
        expected_answer: dict
) -> None:
    """
    Проверка, что поиск по названию фильма
    возвращает только первые 40 результатов
    :return:
    """
    # Загружаем данные в ES
    await es_write_data(es_data)
    time.sleep(1)
    response = await make_get_request('search', query_data)

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']
