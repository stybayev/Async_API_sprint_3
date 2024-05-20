from app.models.base_model import BaseFilm, PaginatedParams
from app.models.persons import Director, Actor, Writer
from typing import Optional, List


class Film(BaseFilm):
    description: Optional[str] = None
    genre: List[str]
    actors_names: List[str]
    writers_names: List[str]
    director: Director
    actors: List[Actor]
    writers: List[Writer]


class Films(BaseFilm, PaginatedParams):
    pass
