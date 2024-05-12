from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Path

from app.models.base_model import BaseMixin
from app.utils.dc_objects import PaginatedParams
from app.models.film import Films
from app.models.persons import BasePersonModel
from app.services.person import get_person_service, PersonsService

router = APIRouter()


@router.get("/{person_id}", response_model=BasePersonModel)
async def get_person_by_id(
        person_id: UUID = Path(..., description="person's ID"),
        person_service: PersonsService = Depends(get_person_service)
) -> BaseMixin:
    """
    Получение персоны по id.

    - **person_id**: id персоны
    """
    person_item = await person_service.get_by_id(person_id)
    if not person_item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='person not found')
    return person_item


@router.get("/", response_model=list[BasePersonModel])
async def person(
        query: str = Query(description='Search query', default=''),
        page_size: int = PaginatedParams.page_size,
        page_number: int = PaginatedParams.page_number,
        person_service: PersonsService = Depends(get_person_service)
) -> list[BasePersonModel]:
    """
    Получение списка персон с пагинацией.

    - **query**: поисковый запрос
    - **page_size**: размер страницы
    - **page_number**: номер страницы
    """
    return await person_service.search_person(query, page_size, page_number)


@router.get("/{person_id}/film", response_model=list[Films])
async def get_person_by_id(
        person_id: UUID = Path(..., description="person's ID"),
        page_size: int = PaginatedParams.page_size,
        page_number: int = PaginatedParams.page_number,
        person_service: PersonsService = Depends(get_person_service)
) -> list[Films]:
    """
    Получение фильмов по id персоны.

    - **person_id**: id персоны
    - **page_size**: размер страницы
    - **page_number**: номер страницы

    """
    return await person_service.get_films(person_id, page_size, page_number)
