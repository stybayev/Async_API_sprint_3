from fastapi import Depends
from uuid import UUID
from app.models.genre import Genre
from app.db.redis import get_redis
from app.db.elastic import get_elastic
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from app.services.base import BaseService


class GenreService(BaseService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)
        self.model = Genre
        self.index_name = "genres"

    async def get_by_id(self, genre_id: UUID) -> Genre | None:
        genre = await self._entity_from_cache(_id=genre_id)

        if not genre:
            genre = await self._get_entity_from_elastic(_id=genre_id)
            if not genre:
                return None
            await self._put_entity_to_cache(entity=genre)
        return genre

    async def _get_entity_from_elastic(self, _id: UUID) -> Genre | None:
        try:
            doc = await self.elastic.get(index=self.index_name, id=_id)
        except NotFoundError:
            return None
        return self.model(**doc["_source"])

    async def _entity_from_cache(self, _id: UUID) -> Genre | None:
        data = await self.redis.get(f"{self.index_name}:{_id}")
        if not data:
            return None
        return self.model.parse_raw(data)

    async def _put_entity_to_cache(self, entity: Genre):
        await self.redis.set(
            f"{self.index_name}:{entity.id}",
            entity.json(),
            self.cache_timeout
        )

    async def list_genres(self, page_size: int, page_number: int) -> list[Genre]:
        params = {"page_size": page_size, "page_number": page_number}
        cached_genres = await self._entities_from_cache(params)
        if not cached_genres:
            cached_genres = await self._get_genres_from_elastic(page_size, page_number)
            if cached_genres:
                await self._put_entities_to_cache(cached_genres, params)
        return cached_genres

    async def _get_genres_from_elastic(self, page_size: int, page_number: int) -> list[Genre]:
        offset = (page_number - 1) * page_size
        try:
            response = await self.elastic.search(
                index=self.index_name,
                body={"from": offset, "size": page_size}
            )
        except NotFoundError:
            return []
        return [self.model(**item['_source']) for item in response['hits']['hits']]


# Dependency Injection function to get the GenreService instance
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
