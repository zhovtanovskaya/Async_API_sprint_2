run_server:
	./src/entrypoint.sh

run_tests:
	pytest ./tests/functional/src

dc_up_dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dc_ps:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml ps

dc_start:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml start $(service)

dc_logs:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -t $(service) | more | less

dc_rebuild:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml rm $(service)
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build $(service)
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d $(service)
