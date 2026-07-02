with source as (
    select raw_json
    from {{ source('raw', 'global__world_production_by_country_raw') }}
)
select
    raw_json:"period"::number(10,0)          as period_year,
    raw_json:"productId"::varchar            as product_id,
    raw_json:"productName"::varchar          as product_name,
    raw_json:"activityId"::varchar           as activity_id,
    raw_json:"activityName"::varchar         as activity_name,
    raw_json:"countryRegionId"::varchar      as country_region_id,
    raw_json:"countryRegionName"::varchar    as country_region_name,
    raw_json:"countryRegionTypeId"::varchar  as country_region_type_id,
    try_to_decimal(raw_json:"value"::varchar, 20, 4) as value,
    raw_json:"unit"::varchar                 as unit,
    raw_json:"dataFlagDescription"::varchar  as data_flag_description
from source