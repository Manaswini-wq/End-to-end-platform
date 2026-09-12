with source as (
    select * from {{ source('retail_raw', 'raw_products') }}
)

select
    product_id,
    product_name,
    category,
    subcategory,
    brand,
    cost_price,
    list_price,
    weight_kg,
    round(list_price - cost_price, 2) as margin,
    round((list_price - cost_price) / nullif(list_price, 0) * 100, 1) as margin_pct
from source
