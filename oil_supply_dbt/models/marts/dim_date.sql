with date_spine as (
    select dateadd(month, seq4(), '1920-01-01'::date) as date_month
    from table(generator(rowcount => 1300))
)

select
    date_month,
    year(date_month)        as year,
    month(date_month)       as month,
    quarter(date_month)     as quarter,
    monthname(date_month)   as month_name
from date_spine
where date_month <= dateadd(month, 1, current_date())