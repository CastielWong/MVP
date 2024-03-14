
init-local-env:
	docker-compose -f dev/docker-compose.yaml --project-directory '${PWD}' up -d local-env database
	# wait for database to be ready
	sleep 20
	docker exec -w /app/integration -it dp-local-env python setup_db.py

unit-test:
	poetry poe test

integration-test:
	docker-compose -f dev/docker-compose.yaml --project-directory '${PWD}' up --exit-code-from ci ci
	docker-compose -f dev/docker-compose.yaml --project-directory '${PWD}' rm -f ci

cleanup:
	docker-compose -f dev/docker-compose.yaml down
	echo y | docker system prune
