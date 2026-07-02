with stocks as (
    select
        period_date,
        duoarea,
        area_name,
        process_code,
        process_name,
        value as stocks_mbbl
    from {{ ref('stg_weekly_stocks') }}
)

select
    period_date,
    duoarea,
    area_name,
    process_code,
    process_name,
    stocks_mbbl
from stocks