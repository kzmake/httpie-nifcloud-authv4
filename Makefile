.PHONY: all fmt install test clean publish

all:
	poetry build

fmt:
	poetry run sh -c 'git ls-files *.py **/*.py | xargs black'

install:
	poetry install

clean:
	rm -rf dist/ src/httpie_nifcloud_authv4.egg-info/ src/__pycache__/

publish:
	poetry publish
