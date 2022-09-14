from uuid import UUID

from .person_base import PersonBase


class Person(PersonBase):
    """Валидатор записи индекса 'person'."""

    role: list[str]
    film_ids: list[UUID] = []
