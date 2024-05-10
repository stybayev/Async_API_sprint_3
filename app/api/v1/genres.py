from fastapi import APIRouter, Depends, Query, Path, HTTPException

from app.db.elastic import get_elastic, AsyncElasticsearch
from app.models.genre import Genre
from http import HTTPStatus
from uuid import UUID

from app.services.base import BaseService
from app.services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def get_genre_by_id(
        genre_id: UUID = Path(..., description="Genre's ID"),
        service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='genre not found')
    return genre


@router.get("/", response_model=list[Genre])
async def genre(
        page_size: int = Query(10, ge=1, description='Pagination page size'),
        page_number: int = Query(1, ge=1, description='Pagination page number'),
        service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """
    Получение списка жанров с пагинацией.

    - **page_size**: размер страницы
    - **page_number**: номер страницы
    """
    return await service.list_genres(page_size, page_number)
