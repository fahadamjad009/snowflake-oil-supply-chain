with refinery as (
    select
        period_date,
        duoarea,
        area_name,
        process_code,
        process_name,
        series_id,
        series_description,
        value,
        units
    from {{ ref('stg_refinery_utilization') }}
)
select * from refinery