
container = example-ci

.PHONY: uninstall clean install build

## packaging
uninstall:
	pip uninstall example_pacakge -y

clean:
	python setup.py clean --all; rm -rf dist/ example_pacakge.egg-info/

install: clean uninstall
	pip install -r requirements.txt
	python setup.py install

## sample configuration for pacakge uploading
#upload:
#	echo "[distutils]" > ~/.pypirc
#	echo "index-servers = local" >> ~/.pypirc
#	echo "[local]" >> ~/.pypirc
#	echo "repository: https://${ARTIFACTOR_URL}/artifactory/api/pypi/${REPO_PYPI}" >> ~/.pypirc
#	echo "username: ${ARTIFACTORY_USERNAME}" >> ~/.pypirc
#	echo "password: ${ARTIFACTORY_PASSWORD}" >> ~/.pypirc
#
#	python setup.py bdist_wheel upload -r local


## development
build-ci:
	docker-compose build --no-cache ci

test:
	docker-compose up --exit-code-from ci ci
	docker-compose down

prune: clean
	rm-rf .mypy_cache/ .pytest_cache/ .coverage results.xml

check-container:
	docker run --name check-example --rm -it example:ci bash
