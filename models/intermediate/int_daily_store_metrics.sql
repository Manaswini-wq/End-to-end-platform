with enriched as (
    select * from {{ ref('int_sales_enriched') }}
)

select
    transaction_date,
    store_id,
    store_name,
    city,
    region,
    count(distinct transaction_id) as transaction_count,
    count(distinct customer_id) as unique_customers,
    sum(net_amount) as revenue,
    sum(profit) as profit,
    round(avg(net_amount), 2) as avg_transaction_value,
    round(avg(discount_pct), 1) as avg_discount,
    sum(quantity) as units_sold,
    count(distinct product_id) as unique_products_sold,
    max(temp_avg_c) as temperature,
    max(weather_condition) as weather
from enriched
group by 1, 2, 3, 4, 5
