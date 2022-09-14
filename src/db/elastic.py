from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    """Функция для внедрения зависимости от AsyncElasticsearch.

    Returns:
        Асинхронный клиент для ElasticSearch.
    """
    return es
