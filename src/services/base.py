from abc import ABC, abstractmethod

from models.elastic.base_model import DBModel


class AbstractObjectService(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> DBModel | None:
        ...
