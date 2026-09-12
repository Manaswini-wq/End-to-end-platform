with source as (
    select * from {{ source('retail_raw', 'raw_inventory') }}
)

select
    store_id,
    product_id,
    quantity_on_hand,
    reorder_point,
    cast(last_restock_date as date) as last_restock_date,
    supplier_lead_days,
    case
        when quantity_on_hand <= 0 then 'out_of_stock'
        when quantity_on_hand <= reorder_point then 'low_stock'
        else 'in_stock'
    end as stock_status,
    quantity_on_hand - reorder_point as stock_buffer
from source
