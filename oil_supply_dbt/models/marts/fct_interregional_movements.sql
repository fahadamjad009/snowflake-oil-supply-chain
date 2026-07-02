with movements as (
    select
        period_date,
        duoarea,
        split_part(duoarea, '-', 1) as origin_padd,
        split_part(duoarea, '-', 2) as destination_padd,
        area_name,
        process_code,
        process_name,
        value as movement_mbbl
    from {{ ref('stg_interregional_movements') }}
)
select * from movements