
SHELL := /bin/bash

CONTAINER = sandbox-checking

start:
	docker-compose up -d

run:
	docker exec -it $(CONTAINER) bash

end:
	docker-compose stop
	echo y | docker system prune
