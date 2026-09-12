.PHONY: ingest dbt quality all

ingest:
	python -m src.ingest_csv
	python -m src.ingest_api
	python -m src.ingest_postgres

dbt:
	cd dbt_project && dbt run --profiles-dir . && dbt test --profiles-dir .

quality:
	python -m data_quality.quality_checks

profile:
	python -m data_quality.profiler

test:
	pytest tests/ -v

all: ingest dbt quality
