"""Upload raw data to GCS data lake with date partitioning."""

from google.cloud import storage
from src.utils import load_config, get_env, today_partition


def upload_to_lake(data_bytes, source_name, file_name):
    config = load_config()
    bucket_name = config["gcp"]["data_lake_bucket"]
    prefix = config["data_lake"]["raw_prefix"]
    path = f"{prefix}/{source_name}/{today_partition()}/{file_name}"

    client = storage.Client(project=get_env("GCP_PROJECT_ID"))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(path)
    blob.upload_from_string(data_bytes)
    print(f"Uploaded gs://{bucket_name}/{path}")
    return f"gs://{bucket_name}/{path}"
