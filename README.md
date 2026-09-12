# End-to-End Data Platform — Single Source of Truth

A complete data platform that ingests from 3 sources (API, CSV, PostgreSQL),
lands data in a GCS data lake, transforms via dbt into a BigQuery star schema,
enforces data quality gates, and serves analytics-ready tables.

## Architecture

```
  Weather API ──┐
  CSV Files ────┼──→ GCS Data Lake ──→ BigQuery Raw ──→ dbt ──→ Star Schema
  PostgreSQL ───┘                                               (BigQuery)
                                                                    │
                                                        ┌───────────┼───────────┐
                                                   dim_stores  fct_sales  fct_inventory
                                                   dim_products  fct_daily_revenue
                                                   dim_dates     fct_inventory_health
```

## Star Schema

```
            ┌─────────────┐
            │  dim_dates   │
            └──────┬──────┘
                   │
┌──────────┐  ┌────▼─────┐  ┌──────────────┐
│dim_stores├──┤fct_sales ├──┤dim_products  │
└──────────┘  └────┬─────┘  └──────────────┘
                   │
          ┌────────▼──────────┐
          │fct_daily_revenue  │
          └───────────────────┘
```

## Tech Stack

| Layer            | Technology              |
|------------------|-------------------------|
| Ingestion        | Python, Requests, Pandas|
| Data Lake        | Google Cloud Storage    |
| Warehouse        | Google BigQuery         |
| Transformation   | dbt                     |
| Orchestration    | Apache Airflow          |
| Data Quality     | Great Expectations      |
| Infrastructure   | Terraform               |

## Quick Start

```bash
pip install -r requirements.txt
make all        # ingest + dbt + quality checks
make profile    # profile all tables
make test       # run unit tests
```
