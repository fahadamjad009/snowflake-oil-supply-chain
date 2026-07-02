with grade_imports as (
    select
        period_date,
        origin_id,
        origin_name,
        origin_type,
        destination_id,
        destination_name,
        grade_id,
        grade_name,
        quantity as quantity_mbbl
    from {{ ref('stg_crude_imports_by_grade') }}
)
select * from grade_imports