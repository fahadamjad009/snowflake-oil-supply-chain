with imports as (
    select
        period_date,
        duoarea,
        area_name,
        series_id,
        series_description,
        value as imports_mbbl
    from {{ ref('stg_us_crude_imports_by_country') }}
)
select * from imports