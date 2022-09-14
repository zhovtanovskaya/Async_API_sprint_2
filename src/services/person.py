"""Доступ к персонам в индексах ElasticSearch."""
from functools import lru_cache
from typing import Iterable

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.base_model import DBModel
from models.person import Person
from services.base import ElasticService


class PersonService(ElasticService):
    """Сервис для доступа к персонам в ElasticSearch."""

    async def search(
            self, query: str, limit: int, offset: int,
            ) -> Iterable[DBModel]:
        """Найти персон по имени и с паджинацией.

        Args:
            query: Поисковый запрос.
            limit: Вернуть столько совпадений.
            offset: Вернуть совпадения, начиная с offset-того по счету.

        Returns:
            Список из size персон, начиная с offset-того совпадения по счету.
        """
        body = {
            'query': {
                'match': {
                    'name': {
                        'query': query,
                        'fuzziness': 'auto',
                    },
                },
            },
        }
        params = {
            'size': limit,
            'from': offset,
        }
        results = await self.elastic.search(
            index=self.index, body=body, params=params)
        hits = results['hits']['hits']
        return [self._to_object(hit) for hit in hits]


@lru_cache()
def get_person_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
        ) -> PersonService:
    """Получить сервис для доступа к персонам.

    Args:
        elastic: Клиент для ElasticSearch.

    Returns:
        Сервис для доступа к персонам из индекса Elastic.
    """
    return PersonService(elastic, 'persons', Person)
