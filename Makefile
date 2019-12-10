.PHONY: all fmt install test clean publish

all:
	python setup.py bdist

fmt:
	git ls-files *.py **/*.py | xargs black

install:
	python setup.py install

clean:
	rm -rf build/ dist/ httpie_aws_authv4.egg-info/

publish:
	python setup.py sdist
	twine upload dist/*
