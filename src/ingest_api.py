"""Ingest weather data from Open-Meteo API (free, no key needed)."""

import requests
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from src.utils import load_config, get_env
from src.data_lake import upload_to_lake


def fetch_weather(city, days=30):
    config = load_config()
    base_url = config["sources"]["weather_api"]["base_url"]
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    resp = requests.get(base_url, params={
        "latitude": city["lat"],
        "longitude": city["lon"],
        "start_date": start,
        "end_date": end,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "America/New_York",
    })
    resp.raise_for_status()
    data = resp.json()["daily"]

    df = pd.DataFrame(data)
    df["city"] = city["name"]
    df["latitude"] = city["lat"]
    df["longitude"] = city["lon"]
    df.rename(columns={"time": "date"}, inplace=True)
    return df


def ingest_weather():
    config = load_config()
    project = get_env("GCP_PROJECT_ID")
    cities = config["sources"]["weather_api"]["cities"]

    all_weather = pd.concat([fetch_weather(c) for c in cities], ignore_index=True)
    print(f"Fetched {len(all_weather)} weather records for {len(cities)} cities")

    # Upload to data lake
    csv_bytes = all_weather.to_csv(index=False).encode()
    upload_to_lake(csv_bytes, "weather", "weather.csv")

    # Load to BigQuery raw
    client = bigquery.Client(project=project)
    dataset = config["bigquery"]["raw_dataset"]
    table_id = f"{project}.{dataset}.raw_weather"

    client.create_dataset(bigquery.Dataset(f"{project}.{dataset}"), exists_ok=True)
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    client.load_table_from_dataframe(all_weather, table_id, job_config=job_config).result()
    print(f"Loaded {len(all_weather)} rows → {table_id}")


if __name__ == "__main__":
    ingest_weather()
