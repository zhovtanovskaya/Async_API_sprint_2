"""Абстрактные сервисы."""

from abc import ABC, abstractmethod

from models.abstract import DBModel


class AbstractDetailsService(ABC):
    """Абстрактный сервис для извлечения объекта из БД."""

    @abstractmethod
    def get_by_id(self, id: str) -> DBModel | None:
        """Получить объект из базы по идентификатору.

        Args:
            id: Уникальный идентификатор объекта в БД.

        Returns:
            Python-представление объекта из БД.
        """
        ...
