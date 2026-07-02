with production as (
    select
        period_year,
        country_region_id,
        country_region_name,
        value as production_tbpd,
        data_flag_description
    from {{ ref('stg_world_production') }}
    where unit = 'TBPD'
)

select
    p.period_year,
    p.country_region_id,
    p.country_region_name,
    p.production_tbpd,
    p.data_flag_description,
    case when p.production_tbpd is null then true else false end as is_missing_data
from production p