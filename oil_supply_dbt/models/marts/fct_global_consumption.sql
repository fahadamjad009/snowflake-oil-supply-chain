with consumption as (
    select
        period_year,
        country_region_id,
        country_region_name,
        value as consumption_tbpd,
        data_flag_description
    from {{ ref('stg_world_consumption') }}
    where unit = 'TBPD'
)

select
    c.period_year,
    c.country_region_id,
    c.country_region_name,
    c.consumption_tbpd,
    c.data_flag_description,
    case when c.consumption_tbpd is null then true else false end as is_missing_data
from consumption c