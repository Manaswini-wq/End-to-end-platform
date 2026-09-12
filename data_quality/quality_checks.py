"""Data quality checks for the Single Source of Truth."""

from google.cloud import bigquery
from src.utils import get_env


def run_checks():
    project = get_env("GCP_PROJECT_ID")
    client = bigquery.Client(project=project)
    dataset = "retail_analytics"
    results = []

    checks = [
        ("no_null_dates", f"SELECT count(*) as c FROM `{project}.{dataset}.fct_sales` WHERE transaction_date IS NULL", lambda r: r == 0),
        ("positive_revenue", f"SELECT count(*) as c FROM `{project}.{dataset}.fct_sales` WHERE net_amount < 0", lambda r: r == 0),
        ("min_row_count", f"SELECT count(*) as c FROM `{project}.{dataset}.fct_sales`", lambda r: r > 10000),
        ("no_orphan_stores", f"SELECT count(*) as c FROM `{project}.{dataset}.fct_sales` s LEFT JOIN `{project}.{dataset}.dim_stores` d ON s.store_id = d.store_id WHERE d.store_id IS NULL", lambda r: r == 0),
        ("no_orphan_products", f"SELECT count(*) as c FROM `{project}.{dataset}.fct_sales` s LEFT JOIN `{project}.{dataset}.dim_products` d ON s.product_id = d.product_id WHERE d.product_id IS NULL", lambda r: r == 0),
        ("inventory_completeness", f"SELECT count(*) as c FROM `{project}.{dataset}.fct_inventory_health`", lambda r: r > 5000),
    ]

    print("\n" + "=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)

    all_passed = True
    for name, query, validator in checks:
        val = list(client.query(query).result())[0][0]
        passed = validator(val)
        if not passed:
            all_passed = False
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}: {val}")
        results.append({"check": name, "passed": passed, "value": val})

    print("=" * 50)
    print(f"Result: {'ALL PASSED' if all_passed else 'FAILURES DETECTED'}")
    return results, all_passed


if __name__ == "__main__":
    _, passed = run_checks()
    exit(0 if passed else 1)
