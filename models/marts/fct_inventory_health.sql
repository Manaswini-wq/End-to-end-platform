with inventory as (
    select * from {{ ref('stg_inventory') }}
),

products as (
    select product_id, category, list_price from {{ ref('stg_products') }}
),

stores as (
    select store_id, store_name, region from {{ ref('stg_stores') }}
)

select
    i.store_id,
    s.store_name,
    s.region,
    i.product_id,
    p.category,
    i.quantity_on_hand,
    i.reorder_point,
    i.stock_status,
    i.stock_buffer,
    i.supplier_lead_days,
    i.last_restock_date,
    date_diff(current_date(), i.last_restock_date, day) as days_since_restock,
    round(i.quantity_on_hand * p.list_price, 2) as inventory_value
from inventory i
left join products p on i.product_id = p.product_id
left join stores s on i.store_id = s.store_id
