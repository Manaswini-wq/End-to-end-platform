with products as (
    select * from {{ ref('stg_products') }}
),

product_stats as (
    select
        product_id,
        sum(quantity) as total_units_sold,
        sum(net_amount) as total_revenue,
        sum(profit) as total_profit,
        count(distinct store_id) as sold_in_stores,
        count(distinct customer_id) as unique_buyers
    from {{ ref('int_sales_enriched') }}
    group by product_id
)

select
    p.*,
    coalesce(ps.total_units_sold, 0) as total_units_sold,
    coalesce(ps.total_revenue, 0) as total_revenue,
    coalesce(ps.total_profit, 0) as total_profit,
    coalesce(ps.sold_in_stores, 0) as sold_in_stores,
    coalesce(ps.unique_buyers, 0) as unique_buyers
from products p
left join product_stats ps on p.product_id = ps.product_id
