"""Абстрактные модели для сервисов."""

from abc import ABC


class DBModel(ABC):
    """Абстрактный класс модели для сервиса.

    Создан для изоляции некоторых контроллеров REST API v1
    от конкретных сервисов БД.
    """

    id: str
