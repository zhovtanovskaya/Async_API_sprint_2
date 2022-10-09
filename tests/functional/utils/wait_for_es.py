"""Модуль для Docker, который дожидается старта Elastic."""

import time

from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings

if __name__ == '__main__':
    hosts = [f'{test_settings.elastic_host}:{test_settings.elastic_port}']
    es_client = Elasticsearch(hosts=hosts, validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
