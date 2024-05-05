from dataclasses import dataclass

from multidict import CIMultiDictProxy


@dataclass
class Response:
    body: dict
    header: CIMultiDictProxy[str]
    status: int
