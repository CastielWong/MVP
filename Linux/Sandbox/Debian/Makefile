
CONTAINER = sandbox-debian

start:
	docker-compose up -d

run:
	docker exec -it $(CONTAINER) bash

stop:
	docker-compose stop
	echo y | docker system prune
