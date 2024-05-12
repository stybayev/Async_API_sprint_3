from fastapi import APIRouter, Depends, Path, HTTPException

from app.models.genre import Genre
from http import HTTPStatus
from uuid import UUID
from app.utils.dc_objects import PaginatedParams
from app.services.genres import GenreService, get_genre_service

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def get_genre_by_id(
        genre_id: UUID = Path(..., description="Genre's ID"),
        service: GenreService = Depends(get_genre_service)) -> Genre:
    genre_item = await service.get_by_id(genre_id)
    if not genre_item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='genre not found')
    return genre_item


@router.get("/", response_model=list[Genre])
async def genre(
        page_size: int = PaginatedParams.page_size,
        page_number: int = PaginatedParams.page_number,
        service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """
    Получение списка жанров с пагинацией.

    - **page_size**: размер страницы
    - **page_number**: номер страницы
    """
    return await service.list_genres(page_size, page_number)
