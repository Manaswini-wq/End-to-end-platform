"""Ingest CSV files into data lake and BigQuery raw layer."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from src.utils import load_config, get_env
from src.data_lake import upload_to_lake


def generate_sales(n=100000):
    np.random.seed(42)
    start = datetime(2023, 1, 1)
    return pd.DataFrame({
        "transaction_id": [f"TXN-{i:07d}" for i in range(n)],
        "store_id": [f"STORE-{np.random.randint(1, 21):03d}" for _ in range(n)],
        "product_id": [f"PROD-{np.random.randint(1, 501):04d}" for _ in range(n)],
        "customer_id": [f"CUST-{np.random.randint(1, 10001):05d}" for _ in range(n)],
        "quantity": np.random.randint(1, 10, n),
        "unit_price": np.round(np.random.uniform(1, 200, n), 2),
        "discount_pct": np.random.choice([0, 5, 10, 15, 20, 25], n),
        "transaction_date": [start + timedelta(days=int(d)) for d in np.random.randint(0, 365, n)],
        "payment_method": np.random.choice(["cash", "credit", "debit", "mobile"], n),
    })


def generate_stores(n=20):
    cities = ["New York", "Chicago", "Los Angeles", "Houston", "Miami",
              "Dallas", "Seattle", "Boston", "Denver", "Atlanta"]
    return pd.DataFrame({
        "store_id": [f"STORE-{i:03d}" for i in range(1, n + 1)],
        "store_name": [f"Store #{i}" for i in range(1, n + 1)],
        "city": [cities[i % len(cities)] for i in range(n)],
        "state": ["NY", "IL", "CA", "TX", "FL", "TX", "WA", "MA", "CO", "GA"] * 2,
        "region": np.random.choice(["northeast", "midwest", "west", "south"], n),
        "store_type": np.random.choice(["flagship", "standard", "outlet"], n),
        "sqft": np.random.randint(2000, 20000, n),
        "open_date": pd.date_range("2015-01-01", periods=n, freq="60D"),
    })


def generate_products(n=500):
    categories = ["electronics", "clothing", "grocery", "home", "sports", "beauty", "toys"]
    return pd.DataFrame({
        "product_id": [f"PROD-{i:04d}" for i in range(1, n + 1)],
        "product_name": [f"Product_{i}" for i in range(1, n + 1)],
        "category": np.random.choice(categories, n),
        "subcategory": [f"sub_{np.random.randint(1,20)}" for _ in range(n)],
        "brand": [f"Brand_{np.random.randint(1, 50)}" for _ in range(n)],
        "cost_price": np.round(np.random.uniform(1, 150, n), 2),
        "list_price": np.round(np.random.uniform(2, 250, n), 2),
        "weight_kg": np.round(np.random.uniform(0.1, 25, n), 2),
    })


def ingest_csvs():
    config = load_config()
    project = get_env("GCP_PROJECT_ID")
    dataset = config["bigquery"]["raw_dataset"]
    client = bigquery.Client(project=project)
    client.create_dataset(bigquery.Dataset(f"{project}.{dataset}"), exists_ok=True)

    tables = {
        "raw_sales": generate_sales(),
        "raw_stores": generate_stores(),
        "raw_products": generate_products(),
    }

    for table_name, df in tables.items():
        # Data lake
        csv_bytes = df.to_csv(index=False).encode()
        upload_to_lake(csv_bytes, table_name.replace("raw_", ""), f"{table_name}.csv")

        # BigQuery
        table_id = f"{project}.{dataset}.{table_name}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        client.load_table_from_dataframe(df, table_id, job_config=job_config).result()
        print(f"Loaded {len(df)} rows → {table_id}")


if __name__ == "__main__":
    ingest_csvs()
