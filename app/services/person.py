import logging
from functools import lru_cache
from typing import List

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from pydantic import ValidationError
from redis.asyncio import Redis

from app.db.elastic import get_elastic
from app.db.redis import get_redis
from app.models.persons import BasePersonModel
from app.models.film import Films
from app.services.base import BaseService
from uuid import UUID

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonsService(BaseService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.model = BasePersonModel
        self.index_name = "persons"

    async def _person_from_cache(self, person_id: UUID) -> BasePersonModel | None:
        data = await self.redis.get(person_id)
        if not data:
            return None

        person = BasePersonModel.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: BasePersonModel):
        await self.redis.set(person.id, person.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_films(self, person_id: UUID,
                        page_size: int = 10,
                        page_number: int = 1) -> List[Films]:
        self.model = Films

        params = {'person_id': str(person_id),
                  'page_size': page_size,
                  'page_number': page_number}

        cached_films = await self._entities_from_cache(params)
        if cached_films:
            return cached_films

        persons = await self._get_persons_from_elastic(person_id, page_size, page_number)
        if persons:
            await self._put_entities_to_cache(persons, params)
        return persons

    async def _get_persons_from_elastic(self, person_id: UUID,
                                        page_size: int = 10,
                                        page_number: int = 1) -> List[Films]:

        offset = (page_number - 1) * page_size
        query_body = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {"director.id": str(person_id)}
                        },
                        {
                            "match": {"actors.id": str(person_id)}
                        },
                        {
                            "match": {"writers.id": str(person_id)}
                        }
                    ]
                }
            },
            "from": offset,
            "size": page_size
        }

        try:
            response = await self.elastic.search(index='movies', body=query_body)
        except Exception as e:
            logging.error(f"Failed to fetch persons from Elasticsearch: {e}")
            logging.error(query_body)
            return []

        films = []
        for hit in response['hits']['hits']:
            film_data = {
                "id": hit["_id"],
                "title": hit["_source"]["title"],
                "imdb_rating": hit["_source"].get("imdb_rating")
            }
            try:
                film = Films(**film_data)
                films.append(film)
            except ValidationError as e:
                logging.error(f"Error validating person data: {e}")
                continue

        return films

    async def search_person(self, query: str,
                            page_size: int = 10,
                            page_number: int = 1) -> list[BasePersonModel]:
        """
        Search for persons by query with pagination and caching.
        """
        params = {"query": query, "page_size": page_size, "page_number": page_number}
        cached_persons = await self._entities_from_cache(params)
        if cached_persons:
            return cached_persons

        persons = await self._search_persons_from_elastic(query, page_size, page_number)
        if persons:
            await self._put_entities_to_cache(persons, params)

        return persons

    async def _search_persons_from_elastic(self, query: str,
                                           page_size: int = 10,
                                           page_number: int = 1
                                           ) -> list[BasePersonModel]:
        offset = (page_number - 1) * page_size
        search_body = {
            "from": offset,
            "size": page_size,
            "query": {
                "match_all": {}
            }
        }

        if query:
            search_body["query"] = {
                "multi_match": {
                    "query": query,
                    "fields": ["full_name"]
                }
            }

        try:
            response = await self.elastic.search(index=self.index_name, body=search_body)
        except Exception as e:
            logging.error(f"Failed to search persons in Elasticsearch: {e}")
            return []

        persons = []
        for hit in response['hits']['hits']:
            try:
                person = BasePersonModel(**hit['_source'])
                persons.append(person)
            except ValidationError as e:
                logging.error(f"Error validating person data: {e}")
                continue

        return persons

    async def get_persons(self) -> list[BasePersonModel]:
        pagination_params = self.pagination.get_pagination_params()
        search_body = {**pagination_params}

        try:
            response = await self.elastic.search(index=self.index_name,
                                                 body=search_body)
        except Exception as e:
            logging.error(f"Failed to search persons in Elasticsearch: {e}")
            return []

        persons = []
        for hit in response['hits']['hits']:
            try:
                person = BasePersonModel(**hit['_source'])
                persons.append(person)
            except ValidationError as e:
                logging.error(f"Error validating person data: {e}")
                continue

        return persons


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonsService:
    return PersonsService(redis, elastic)
