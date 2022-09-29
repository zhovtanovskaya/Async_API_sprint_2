from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.elastic.genre import Genre
from models.elastic.person import Person
from services.elastic.base import ElasticService
from services.elastic.film import FilmService
from services.elastic.person import PersonService


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    """Вернуть сервис для работы с эндпоинтами /films.

    Args:
        redis: Соединение с redis.
        elastic: Соединение с elasticsearch.

    Returns:
        Сервис, обслуживающий эндпоинты фильмов.
    """
    return FilmService(redis, elastic)


@lru_cache()
def get_genre_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticService:
    """Получить сервис для доступа к жанрам.

    Args:
        elastic: Клиент для ElasticSearch.

    Returns:
        Сервис для доступа к жанрам в Elastic.
    """
    return ElasticService(elastic, 'genres', Genre)


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
