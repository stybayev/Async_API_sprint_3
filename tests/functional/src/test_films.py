import json

import pytest

from tests.functional.settings import test_settings
from tests.functional.conftest import event_loop, es_add_film, es_client, session_client


class TestFilms:
    @pytest.mark.asyncio
    async def test_get_film_by_id(self, session_client, es_add_film):
        url = test_settings.service_url + f'/api/v1/films/{es_add_film["id"]}'
        response = await session_client.get(url)
        body = await response.json()
        status = response.status

        assert status == 200
        assert body['uuid'] == es_add_film["id"]

    @pytest.mark.asyncio
    async def test_get_film_by_not_existing_id(self, session_client):
        url = test_settings.service_url + f'/api/v1/films/123e4567-e89b-12d3-a456-426655440000'
        response = await session_client.get(url)
        body = await response.json()
        status = response.status

        assert status == 404
        assert body == {'detail': 'film not found'}

