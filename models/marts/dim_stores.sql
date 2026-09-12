with stores as (
    select * from {{ ref('stg_stores') }}
),

store_stats as (
    select
        store_id,
        min(transaction_date) as first_sale_date,
        max(transaction_date) as last_sale_date,
        count(distinct transaction_id) as lifetime_transactions,
        sum(net_amount) as lifetime_revenue
    from {{ ref('int_sales_enriched') }}
    group by store_id
)

select
    s.store_id,
    s.store_name,
    s.city,
    s.state,
    s.region,
    s.store_type,
    s.sqft,
    s.open_date,
    s.months_open,
    coalesce(ss.lifetime_transactions, 0) as lifetime_transactions,
    coalesce(ss.lifetime_revenue, 0) as lifetime_revenue,
    round(coalesce(ss.lifetime_revenue, 0) / nullif(s.sqft, 0), 2) as revenue_per_sqft
from stores s
left join store_stats ss on s.store_id = ss.store_id
