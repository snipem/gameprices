# .PHONY: env
# SHELL := /bin/bash

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	. venv/bin/activate; pip install -Ur test_requirements.txt
	touch venv/bin/activate

test: venv
	(. venv/bin/activate; pytest gameprices/test)

clean:
	rm -rf venv

deps:
	python3 -m pip install virtualenv