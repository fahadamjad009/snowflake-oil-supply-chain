with source as (
    select raw_json
    from {{ source('raw', 'global__crude_oil_imports_by_country_grade_raw') }}
)
select
    try_to_date(raw_json:"period"::varchar || '-01', 'YYYY-MM-DD') as period_date,
    raw_json:"originId"::varchar             as origin_id,
    raw_json:"originName"::varchar           as origin_name,
    raw_json:"originType"::varchar           as origin_type,
    raw_json:"destinationId"::varchar        as destination_id,
    raw_json:"destinationName"::varchar      as destination_name,
    raw_json:"gradeId"::varchar              as grade_id,
    raw_json:"gradeName"::varchar            as grade_name,
    raw_json:"quantity"::number(20,4)        as quantity,
    raw_json:"quantity-units"::varchar       as quantity_units
from source