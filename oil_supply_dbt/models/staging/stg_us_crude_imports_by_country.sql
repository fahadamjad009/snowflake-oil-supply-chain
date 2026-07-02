with source as (
    select raw_json
    from {{ source('raw', 'infrastructure__us_crude_imports_by_country_of_origin_raw') }}
)
select
    try_to_date(raw_json:"period"::varchar || '-01', 'YYYY-MM-DD') as period_date,
    raw_json:"duoarea"::varchar              as duoarea,
    raw_json:"area-name"::varchar            as area_name,
    raw_json:"product"::varchar              as product_code,
    raw_json:"product-name"::varchar         as product_name,
    raw_json:"process"::varchar              as process_code,
    raw_json:"process-name"::varchar         as process_name,
    raw_json:"series"::varchar               as series_id,
    raw_json:"series-description"::varchar   as series_description,
    raw_json:"value"::number(20,4)           as value,
    raw_json:"units"::varchar                as units
from source