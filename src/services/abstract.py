from abc import ABC, abstractmethod

from models.abstract import DBModel


class AbstractDetailsService(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> DBModel | None:
        ...
