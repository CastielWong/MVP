
CONTAINER = mvp-ocr

start:
	docker-compose up -d

run:
	docker exec -it $(CONTAINER) bash

scan-image:
	cp ~/Downloads/_question.png images/question.png
	docker exec -it $(CONTAINER) python -m src

stop:
	docker-compose stop
	echo y | docker system prune
