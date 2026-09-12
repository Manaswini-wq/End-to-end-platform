FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["bash", "-c", "python -m src.ingest_csv && python -m src.ingest_api && python -m src.ingest_postgres && cd dbt_project && dbt run --profiles-dir . && dbt test --profiles-dir . && cd .. && python -m data_quality.quality_checks"]
