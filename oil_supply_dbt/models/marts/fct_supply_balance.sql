with balance as (
    select
        period_date,
        process_code,
        value
    from {{ ref('stg_national_balance') }}
)

select
    period_date,
    max(case when process_code = 'FPF' then value end) as field_production_mbbl,
    max(case when process_code = 'YIR' then value end) as refinery_net_input_mbbl,
    max(case when process_code = 'VPP' then value end) as product_supplied_mbbl,
    max(case when process_code = 'SAE' then value end) as ending_stocks_mbbl,
    max(case when process_code = 'SCG' then value end) as stock_change_mbbl,
    max(case when process_code = 'VUA' then value end) as supply_adjustment_mbbl,
    max(case when process_code = 'TVP' then value end) as transfers_to_crude_supply_mbbl
from balance
group by period_date
order by period_date