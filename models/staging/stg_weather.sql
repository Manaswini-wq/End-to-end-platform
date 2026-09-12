with source as (
    select * from {{ source('retail_raw', 'raw_weather') }}
)

select
    cast(date as date) as weather_date,
    city,
    temperature_2m_max as temp_max_c,
    temperature_2m_min as temp_min_c,
    round((temperature_2m_max + temperature_2m_min) / 2, 1) as temp_avg_c,
    precipitation_sum as precipitation_mm,
    windspeed_10m_max as wind_max_kmh,
    case
        when precipitation_sum > 10 then 'heavy_rain'
        when precipitation_sum > 2 then 'light_rain'
        else 'clear'
    end as weather_condition
from source
