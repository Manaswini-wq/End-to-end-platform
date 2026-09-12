"""Ingest inventory data from PostgreSQL (or simulate it)."""

import numpy as np
import pandas as pd
from google.cloud import bigquery
from src.utils import load_config, get_env
from src.data_lake import upload_to_lake


def generate_inventory(n_products=500, n_stores=20):
    """Simulate inventory snapshot (replaces Postgres in demo mode)."""
    np.random.seed(42)
    rows = []
    for s in range(1, n_stores + 1):
        for p in range(1, n_products + 1):
            rows.append({
                "store_id": f"STORE-{s:03d}",
                "product_id": f"PROD-{p:04d}",
                "quantity_on_hand": np.random.randint(0, 200),
                "reorder_point": np.random.randint(10, 50),
                "last_restock_date": pd.Timestamp("2023-01-01") + pd.Timedelta(days=int(np.random.randint(0, 365))),
                "supplier_lead_days": np.random.randint(1, 14),
            })
    return pd.DataFrame(rows)


def ingest_inventory():
    config = load_config()
    project = get_env("GCP_PROJECT_ID")
    dataset = config["bigquery"]["raw_dataset"]

    df = generate_inventory()
    print(f"Generated {len(df)} inventory records")

    csv_bytes = df.to_csv(index=False).encode()
    upload_to_lake(csv_bytes, "inventory", "inventory.csv")

    client = bigquery.Client(project=project)
    table_id = f"{project}.{dataset}.raw_inventory"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    client.load_table_from_dataframe(df, table_id, job_config=job_config).result()
    print(f"Loaded {len(df)} rows → {table_id}")


if __name__ == "__main__":
    ingest_inventory()
