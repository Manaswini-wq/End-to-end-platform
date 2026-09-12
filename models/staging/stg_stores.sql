with source as (
    select * from {{ source('retail_raw', 'raw_stores') }}
)

select
    store_id,
    store_name,
    city,
    state,
    region,
    store_type,
    sqft,
    cast(open_date as date) as open_date,
    date_diff(current_date(), cast(open_date as date), month) as months_open
from source
