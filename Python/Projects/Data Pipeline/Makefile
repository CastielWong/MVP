

unit-test:
	poetry poe test

integration-test:
	docker-compose -f dev/docker-compose.yaml --project-directory '${PWD}' up --exit-code-from ci ci
	docker-compose -f dev/docker-compose.yaml --project-directory '${PWD}' rm -f ci

cleanup-test:
	docker-compose -f dev/docker-compose.yaml down
	docker system prune
