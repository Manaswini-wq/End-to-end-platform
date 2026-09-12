with sales as (
    select * from {{ ref('stg_sales') }}
),

stores as (
    select * from {{ ref('stg_stores') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

weather as (
    select * from {{ ref('stg_weather') }}
)

select
    s.transaction_id,
    s.transaction_date,
    s.store_id,
    st.store_name,
    st.city,
    st.region,
    st.store_type,
    s.product_id,
    p.product_name,
    p.category,
    p.brand,
    s.customer_id,
    s.quantity,
    s.unit_price,
    s.discount_pct,
    s.gross_amount,
    s.net_amount,
    round(s.quantity * p.cost_price, 2) as cost_of_goods,
    round(s.net_amount - (s.quantity * p.cost_price), 2) as profit,
    s.payment_method,
    w.temp_avg_c,
    w.precipitation_mm,
    w.weather_condition
from sales s
left join stores st on s.store_id = st.store_id
left join products p on s.product_id = p.product_id
left join weather w on st.city = w.city and s.transaction_date = w.weather_date
