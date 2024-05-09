import orjson

from pydantic import BaseModel
from typing import Callable, Optional, Any
from app.models.base_model import BaseMixin, orjson_dumps
from uuid import UUID


class Genre(BaseMixin):
    id: UUID
    name: str
    description: Optional[str] = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
