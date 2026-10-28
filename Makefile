.PHONY: install test lint dbt-debug dbt-build train api docker-build

install:
	python -m pip install -r requirements-dev.txt

test:
	pytest -q

lint:
	ruff check src tests airflow

dbt-debug:
	cd dbt && dbt debug --profiles-dir .

dbt-build:
	cd dbt && dbt build --profiles-dir .

train:
	python -m src.train

api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8080

docker-build:
	docker build -t retail-demand-api .
