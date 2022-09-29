import logging
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError

from models.elastic.film import Film
from models.elastic.film_base import FilmBase
from services.abstract import AbstractObjectService


class FilmService(AbstractObjectService):
    """Сервис по получению данных по эндпоинтам /films."""

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        """Инициализировать сервис, установив соединение с ES.

        Args:
            elastic: соединение с Elasticsearch.

        Returns:
            None.
        """
        self.elastic = elastic
        self.sort_fields = ['imdb_rating',]

    async def get_by_id(self, id: str) -> Film | None:
        """Найти фильм в базе данных elasticsearch.

        Args:
            id: uuid фильма.

        Returns:
            Объект типа Film или None, если фильм не найден.
        """
        try:
            doc = await self.elastic.get('movies', id)
        except NotFoundError:
            return None
        logging.info(f'got film from elasticsearch {doc}')
        return Film(**doc['_source'])

    async def get_films_list(
        self,
        page_number: int,
        page_size: int,
        sort: str,
        filter_genre: str,
        query: str = '',
    ) -> list[FilmBase]:
        """Получить список фильмов.

        Args:
            page_size: Количество фильмов.
            pase_number: Отступ в общем списке фильмов по номеру страницы.
            sort: Сортировка по названию поля. "-" в начале для обратной сортировки.
            filter_genre: uuid жанра, к которому должны принадлежать фильмы.
            query: Строка поиска.
            film_service: Сервис по получению фильмов.

        Returns:
            Список объектов FilmBase.
        """
        request_body = {
            'size': page_size,
            'from': page_number * page_size,
            'query': {
                'bool': {
                    'filter': [
                    ],
                },
            },
            'sort': {},
        }

        await self._set_sorting(request_body, sort)
        await self._set_filtering(request_body, filter_genre)
        await self._set_searching(request_body, query)

        logging.info(f'es request body: {request_body}')

        docs = await self.elastic.search(
            index='movies',
            body=request_body,
        )

        logging.info("Got %d hits" % len(docs['hits']['hits']))

        films = [FilmBase(**doc['_source']) for doc in docs['hits']['hits']]
        return films

    async def _set_sorting(self, request_body: dict, sort: str) -> None:
        """Добавить словарь с параметрами сортировки в словарь request_body.

        Args:
            request_body: тело реквеста, в котором будет добавлена сортировка.
            sort: строка, пришедшая в запросе.

        Returns:
            None.
        """
        if sort:
            s_order = 'desc' if sort.startswith('-') else 'asc'
            s_field = sort.removeprefix('-')
            if s_field in self.sort_fields:
                request_body['sort'][s_field] = {'order': s_order}
        request_body['sort']['title.raw'] = {'order': 'asc'}

    async def _set_filtering(self, request_body: dict, genre_filter: str) -> None:
        """Добавить словарь с параметрами фильтрации в словарь request_body.

        Args:
            request_body: тело реквеста, в котором будет добавлена сортировка.
            genre_filter: название жанра, пришедшее в запросе.

        Returns:
            None.
        """
        if not genre_filter:
            return

        request_body['query']['bool']['filter'].append({
            'nested': {
                'path': 'genres',
                'query': {
                    'bool': {
                        'filter': {
                            'term': {
                                'genres.id': genre_filter
                            }
                        }
                    }
                }
            }
        })

    async def _set_searching(self, request_body: dict, query: str) -> None:
        """Добавить словарь с параметрами поиска.

        Args:
            request_body: тело реквеста, в котором будет добавлена сортировка.
            sort: строка, пришедшая в запросе.

        Returns:
            None.
        """
        if not query:
            return

        request_body['query'] = {
            # 'query': {
                'multi_match': {
                    'query': query,
                    'fields': [
                        'title',
                        'description',
                    ],
                    'type': 'best_fields',
                }
            # }
        }

    async def get_by_ids(self, ids: list[UUID]) -> list[FilmBase]:
        """Получить список фильмов без деталей по ID.

        Args:
            ids: Список ID фильмов.

        Returns:
            Список фильмов без деталей.
        """
        body = {
            'query': {
                'ids': {'values': [str(id) for id in ids]},
            },
        }
        results = await self.elastic.search(index='movies', body=body)
        hits = results['hits']['hits']
        return [FilmBase(**hit['_source']) for hit in hits]
