{% macro generate_date_spine(start_date, end_date) %}

with date_spine as (
    select
        date_add(date '{{ start_date }}', interval offset day) as date_day
    from unnest(generate_array(
        0,
        date_diff(date '{{ end_date }}', date '{{ start_date }}', day)
    )) as offset
)

select
    date_day,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day_of_month,
    extract(dayofweek from date_day) as day_of_week,
    format_date('%A', date_day) as day_name,
    format_date('%B', date_day) as month_name,
    extract(quarter from date_day) as quarter,
    extract(week from date_day) as week_of_year,
    case when extract(dayofweek from date_day) in (1, 7) then true else false end as is_weekend
from date_spine

{% endmacro %}
