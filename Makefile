.PHONY: deploy fury dist clean

include .env
export

dist:
	pipenv run python setup.py bdist_wheel

fury: clean dist
	(export VERSION=`python -c "import coworks;print(coworks.__version__)"`;\
	curl -F package=@dist/coworks-$$VERSION-py2.py3-none-any.whl https://$$FURY_TOKEN@push.fury.io/gdoumenc;\
	unset VERSION)

deploy: clean dist
	pipenv run twine upload dist/*

deploy-test: clean dist
	pipenv run twine upload --repository testpypi dist/*

plugins.zip: coworks/operators.py
	zip -r build/plugins.zip coworks/operators.py

clean:
	rm -rf dist build coworks.egg-info .pytest_cache
	find . -type f -name \*.pyc -delete
	find . -type d -name __pycache__ -exec rm -rf {} \; || true
