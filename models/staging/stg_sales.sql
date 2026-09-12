with source as (
    select * from {{ source('retail_raw', 'raw_sales') }}
)

select
    transaction_id,
    store_id,
    product_id,
    customer_id,
    quantity,
    unit_price,
    discount_pct,
    cast(transaction_date as date) as transaction_date,
    payment_method,
    round(quantity * unit_price, 2) as gross_amount,
    round(quantity * unit_price * (1 - discount_pct / 100), 2) as net_amount
from source
where quantity > 0 and unit_price > 0
