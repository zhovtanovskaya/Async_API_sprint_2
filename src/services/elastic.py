from typing import Iterable

from elasticsearch import AsyncElasticsearch, NotFoundError

from models.elastic.base_model import DBModel
from services.base import AbstractService


class ElasticService(AbstractService):
    """Сервис для получения объектов из индексов Elastic объектов."""

    def __init__(self, elastic: AsyncElasticsearch, index: str, db_model: DBModel):
        self.elastic = elastic
        self.index = index
        self.db_model = db_model

    def _to_object(self, doc: dict) -> DBModel:
        """Преобразовать документ индекса Elastic в объект."""
        return self.db_model(**doc['_source'])

    async def get_by_id(self, id: str) -> DBModel | None:
        """Получить жанр по ID.

        Args:
            id: UUID жанра.

        Returns:
            Экземпляр Genre.
        """
        try:
            doc = await self.elastic.get(self.index, id)
        except NotFoundError:
            return None
        return self._to_object(doc)

    async def get_all(self) -> Iterable[DBModel]:
        """Получить все записи в индексе.

        Returns:
            Все объекты в виде списка.
        """
        results = await self.elastic.search(index=self.index)
        hits = results['hits']['hits']
        return [self._to_object(hit) for hit in hits]