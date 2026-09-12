select store_id, product_id, quantity_on_hand
from {{ ref('fct_inventory_health') }}
where quantity_on_hand < 0
