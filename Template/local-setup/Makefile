
# alias make='make -f tmp_local/Makefile'
# DIR_WORKING := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

SHELL := /bin/bash

.PHONY: run

DIR_LOCAL := "tmp_local"
DIR_VOLUME := "$(DIR_LOCAL)/mount"

IMAGE_NAME := "demo-xxx"
CONTAINER_NAME := "demo-xxx"


build:
    set -a; source $(DIR_LOCAL)/.env; set +a; \
    docker build -t ${IMAGE_NAME} \
        --build-arg HTTPS_PROXY=$${HTTPS_PROXY} \
        -f Dockerfile \
        .

start: build
    docker run --name $(CONTAINER_NAME) \
        --volume ./$(DIR_VOLUME):/external/ \
        -d $(IMAGE_NAME) \
        tail -f /dev/null

copy:
    docker cp ./data.csv $(CONTAINER_NAME):/external

run:
    docker exec -it $(CONTAINER_NAME) bash

end:
    docker stop $(CONTAINER_NAME)
    docker rm $(CONTAINER_NAME)

delete:
    docker rmi $(IMAGE_NAME)

clean:
    echo y | docker system prune

# =============================================================================

TAG_ANNOTATION:="annotate git tag"
IMAGE_PUSHED:="major.minor.patch-x.y"

tag-delete:
    @if git rev-parse "$(IMAGE_PUSHED)" >/dev/null 2>&1; then \
        git tag -d $(IMAGE_PUSHED); \
    else \
        echo "Tag $(IMAGE_PUSHED) doesn't exist, skipping deletion"; \
    fi

tagging: tag-delete
    git tag $(IMAGE_PUSHED)
    git push origin $(IMAGE_PUSHED) -uf

tag-m: tag-delete
    git tag $(IMAGE_PUSHED) -m $(TAG_ANNOTATION)
    git push origin $(IMAGE_PUSHED) -uf
