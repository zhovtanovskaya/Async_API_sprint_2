from typing import Iterable

from models.elastic.base_model import ElasticModel
from services.elastic.base import ElasticService


class PersonService(ElasticService):
    """Сервис для доступа к персонам в ElasticSearch."""

    async def search(
            self, query: str, limit: int, offset: int,
            ) -> Iterable[ElasticModel]:
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
