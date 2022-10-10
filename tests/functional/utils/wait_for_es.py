"""Модуль для Docker, который дожидается старта Elastic."""

from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings
from tests.functional.utils.backoff import backoff


@backoff(exceptions=(ConnectionError,))
def ping_elastic(hosts: list[str]):
    client = Elasticsearch(hosts=hosts, validate_cert=False, use_ssl=False)
    if not client.ping():
        raise ConnectionError()


if __name__ == '__main__':
    hosts = [f'{test_settings.elastic_host}:{test_settings.elastic_port}']
    ping_elastic(hosts)
