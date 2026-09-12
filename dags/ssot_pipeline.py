"""Airflow DAG: Ingest all sources → dbt → Quality checks."""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    dag_id="ssot_retail_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["production", "ssot"],
) as dag:

    ingest_csv = PythonOperator(
        task_id="ingest_csv",
        python_callable=lambda: __import__("src.ingest_csv", fromlist=["ingest_csvs"]).ingest_csvs(),
    )

    ingest_api = PythonOperator(
        task_id="ingest_weather",
        python_callable=lambda: __import__("src.ingest_api", fromlist=["ingest_weather"]).ingest_weather(),
    )

    ingest_pg = PythonOperator(
        task_id="ingest_inventory",
        python_callable=lambda: __import__("src.ingest_postgres", fromlist=["ingest_inventory"]).ingest_inventory(),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /app/dbt_project && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /app/dbt_project && dbt test --profiles-dir .",
    )

    quality = PythonOperator(
        task_id="quality_checks",
        python_callable=lambda: __import__("data_quality.quality_checks", fromlist=["run_checks"]).run_checks(),
    )

    [ingest_csv, ingest_api, ingest_pg] >> dbt_run >> dbt_test >> quality
