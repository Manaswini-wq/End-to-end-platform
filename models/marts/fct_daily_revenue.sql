select
    transaction_date,
    store_id,
    store_name,
    city,
    region,
    transaction_count,
    unique_customers,
    revenue,
    profit,
    avg_transaction_value,
    avg_discount,
    units_sold,
    unique_products_sold,
    temperature,
    weather
from {{ ref('int_daily_store_metrics') }}
