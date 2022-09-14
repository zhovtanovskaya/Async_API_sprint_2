run_server:
	./src/entrypoint.sh

docker_up_dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
