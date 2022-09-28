from abc import ABC, abstractmethod
from typing import Iterable

from models.base_model import DBModel


class AbstractService(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> DBModel | None:
        ...

    @abstractmethod
    def get_all(self) -> Iterable[DBModel]:
        ...
