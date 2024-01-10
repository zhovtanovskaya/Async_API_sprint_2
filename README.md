# REST API для онлайн-кинотеатра

Проект написан на FastAPI и ElasticSearch в качестве базы данных. Представляет собой REST API для получения списка фильмов, жанров и персон (актеров, режиссеров...). Все ответы на запросы кэшируются в Redis. Средствами ElasticSearch обеспечивается полнотекстовый поиск по фильмам.

Вызовы к REST API покрыты функциональными тестами.

# Настройка окружения

Создайте пустой `.env.docker` через копирование:

```
cp .env.docker.example .env.docker   # Окружение для контейнеров Docker Compose.
```

Затем впишите в него параметры подключения к базам данных.

## Запуск Docker, сервера AsyncAPI и тестов

```
make dc_up_dev      # Создать и запустить контейнеры.
make run_server     # Запустить сервер на 8000 порте на хосте для разработки.
make run_tests      # Выполнить тесты сервера на хосте.
```

Больше коротких команд смотри в Makefile.

# Примечание. Связанные проекты

[Ссылка](https://github.com/zhovtanovskaya/Async_API_sprint_2) на репозиторий с первой проектной работой по AsyncAPI.
[Ссылка](https://github.com/zhovtanovskaya/new_admin_panel_sprint_3) на репозиторий с проектной работой ETL из PostgreSQL в ElasticSearch.  В ETL вносились правки, нужные AsyncAPI.  И на GitHub этот репозиторий связан с [образом](https://github.com/zhovtanovskaya/new_admin_panel_sprint_3/pkgs/container/new_admin_panel_sprint_3_etl) ETL для Docker Compose в проекте AsyncAPI.
