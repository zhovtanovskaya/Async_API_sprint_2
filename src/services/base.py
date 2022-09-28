from abc import ABC, abstractmethod

from models.base_model import DBModel


class AbstractStorage(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> DBModel | None:
        ...

    @abstractmethod
    def get_all(self) -> list[DBModel]:
        ...
