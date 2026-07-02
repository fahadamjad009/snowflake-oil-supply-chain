with source as (
    select raw_json
    from {{ source('raw', 'storage__weekly_stocks_by_padd_national_raw') }}
)
select
    raw_json:"period"::date                  as period_date,
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