"""Доступ к жанрам в индексах ElasticSearch."""
from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models.elastic.genre import Genre
from services.elastic import ElasticService


class GenreService(ElasticService):
    """Сервис для доступа к жанрам в индексе ElasticSearch."""


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
