test:
	python3 -m pytest

test_deps:
	python3 -m pip install pytest

coverage:
	python3 -m pytest --spec --instafail --cov=gameprices --cov-report html gameprices/test

coverage_deps:
	python3 -m pip install -r coverage_requirements.txt
