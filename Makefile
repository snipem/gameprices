.PHONY: dist

install:
	pip3 install .

test: test_deps
	python3 -m pytest

test_deps:
	python3 -m pip install pytest

coverage:
	python3 -m pytest --spec --instafail --cov=gameprices --cov-report html gameprices/test

coverage_deps:
	python3 -m pip install -r coverage_requirements.txt

venv:
	python3 -m venv .venv
	echo "run; . .venv/bin/activate"

dist:
	rm dist/* || true
	python3 -m pip install pypandoc twine wheel setuptools
	python3 setup.py sdist

upload: dist
	python3 -m twine upload dist/*
