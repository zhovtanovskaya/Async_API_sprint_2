import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi.applications import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from availability.backoff import backoff
from core.config import settings
from db import elastic, redis

app = FastAPI(
    title='Read-only API для онлайн-кинотеатра',
    description='Получение фильмов, жанров, персон.',
    version='1.0.0',
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
@backoff(exceptions=(ConnectionRefusedError,))
async def startup():
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.elastic_host}:{settings.elastic_port}'])
    logging.debug(f'connected to elasticsearch by {settings.elastic_host}:{settings.elastic_port}')

    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    logging.debug(f'connected to redis by {settings.redis_host}:{settings.redis_port}')


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


API_V1_ROOT = '/api/v1'
app.include_router(films.router, prefix=f'{API_V1_ROOT}/films', tags=['films'])
app.include_router(genres.router, prefix=f'{API_V1_ROOT}/genres', tags=['genres'])
app.include_router(
    persons.router, prefix=f'{API_V1_ROOT}/persons', tags=['persons'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
