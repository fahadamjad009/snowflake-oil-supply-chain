with cushing as (
    select
        period_date,
        duoarea,
        area_name,
        value as stocks_mbbl
    from {{ ref('stg_cushing_storage') }}
)

select
    period_date,
    duoarea,
    area_name,
    stocks_mbbl
from cushing