run_server:
	./src/entrypoint.sh

run_tests:
	pytest ./tests/functional/src

dc_up_dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dc_start:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml start

dc_logs:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml logs -t | more | less
