from src.ingest_csv import generate_sales, generate_stores, generate_products
from src.ingest_postgres import generate_inventory


def test_sales_schema():
    df = generate_sales(100)
    assert len(df) == 100
    assert set(df.columns) >= {"transaction_id", "store_id", "product_id", "quantity", "unit_price"}


def test_no_null_ids():
    df = generate_sales(1000)
    assert df["transaction_id"].notna().all()
    assert df["store_id"].notna().all()


def test_stores_unique():
    df = generate_stores(20)
    assert df["store_id"].nunique() == 20


def test_products_positive_price():
    df = generate_products(100)
    assert (df["list_price"] > 0).all()
    assert (df["cost_price"] > 0).all()


def test_inventory_shape():
    df = generate_inventory(10, 5)
    assert len(df) == 50
    assert (df["quantity_on_hand"] >= 0).all()
