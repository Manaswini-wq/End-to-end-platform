"""Profile BigQuery tables — row counts, nulls, distributions."""

from google.cloud import bigquery
from src.utils import get_env


def profile_table(dataset, table):
    project = get_env("GCP_PROJECT_ID")
    client = bigquery.Client(project=project)
    full_table = f"{project}.{dataset}.{table}"

    # Row count
    count = list(client.query(f"SELECT count(*) FROM `{full_table}`").result())[0][0]

    # Column stats
    schema = client.get_table(full_table).schema
    print(f"\n{'=' * 60}")
    print(f"PROFILE: {full_table} ({count:,} rows)")
    print(f"{'=' * 60}")

    for field in schema:
        null_q = f"SELECT countif({field.name} IS NULL) FROM `{full_table}`"
        nulls = list(client.query(null_q).result())[0][0]
        null_pct = round(nulls / count * 100, 1) if count > 0 else 0
        print(f"  {field.name:<30} {field.field_type:<12} nulls: {nulls:>6} ({null_pct}%)")


if __name__ == "__main__":
    for table in ["fct_sales", "fct_daily_revenue", "dim_stores", "dim_products", "fct_inventory_health"]:
        profile_table("retail_analytics", table)
