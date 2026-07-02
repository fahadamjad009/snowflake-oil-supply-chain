CREATE WAREHOUSE IF NOT EXISTS oil_supply_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE DATABASE IF NOT EXISTS oil_supply_chain;

CREATE SCHEMA IF NOT EXISTS oil_supply_chain.raw;
CREATE SCHEMA IF NOT EXISTS oil_supply_chain.staging;
CREATE SCHEMA IF NOT EXISTS oil_supply_chain.marts;

USE WAREHOUSE oil_supply_wh;
USE DATABASE oil_supply_chain;
USE SCHEMA raw;

SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();

USE WAREHOUSE oil_supply_wh;
USE DATABASE oil_supply_chain;
USE SCHEMA raw;

CREATE OR REPLACE FILE FORMAT json_format
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE;

CREATE OR REPLACE STAGE eia_stage
  FILE_FORMAT = json_format;

SELECT CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME(), CURRENT_USER();  

SELECT raw_json FROM storage__cushing_ok_padd_tank_farm_stocks_raw LIMIT 3;

SELECT * FROM oil_supply_chain.staging.stg_cushing_storage LIMIT 5;

SELECT * FROM oil_supply_chain.staging.stg_world_production
WHERE country_region_id = 'SAU'
ORDER BY period_year DESC
LIMIT 5;

SELECT period_year, country_region_id, value, unit, data_flag_description
FROM oil_supply_chain.staging.stg_world_production
WHERE country_region_id = 'SAU'
ORDER BY period_year DESC
LIMIT 6;

DROP TABLE IF EXISTS oil_supply_chain.staging_marts.dim_date;
DROP SCHEMA IF EXISTS oil_supply_chain.staging_marts;

SELECT * FROM oil_supply_chain.marts.fct_global_production
WHERE country_region_id = 'SAU'
ORDER BY period_year DESC
LIMIT 5;

SELECT DISTINCT unit FROM oil_supply_chain.staging.stg_world_consumption;

SELECT DISTINCT process_code, process_name
FROM oil_supply_chain.staging.stg_national_balance
ORDER BY process_name;

SELECT * FROM oil_supply_chain.marts.fct_supply_balance
ORDER BY period_date DESC
LIMIT 3;

SELECT 'weekly_stocks' as src, min(period_date) as min_date, max(period_date) as max_date, count(*) as n
FROM oil_supply_chain.staging.stg_weekly_stocks
UNION ALL
SELECT 'cushing_stocks' as src, min(period_date), max(period_date), count(*)
FROM oil_supply_chain.staging.stg_cushing_storage;

USE ROLE ACCOUNTADMIN;

CREATE NETWORK RULE IF NOT EXISTS pypi_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'pypi.python.org', 'files.pythonhosted.org');

CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE;

COPY INTO @~/exports/fct_supply_balance.csv
FROM OIL_SUPPLY_CHAIN.MARTS.FCT_SUPPLY_BALANCE
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' NULL_IF = ('') COMPRESSION = NONE)
HEADER = TRUE
OVERWRITE = TRUE
SINGLE = TRUE;

COPY INTO @~/exports/fct_global_production.csv
FROM OIL_SUPPLY_CHAIN.MARTS.FCT_GLOBAL_PRODUCTION
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' NULL_IF = ('') COMPRESSION = NONE)
HEADER = TRUE
OVERWRITE = TRUE
SINGLE = TRUE;

COPY INTO @~/exports/fct_storage_cushing.csv
FROM OIL_SUPPLY_CHAIN.MARTS.FCT_STORAGE_CUSHING
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' NULL_IF = ('') COMPRESSION = NONE)
HEADER = TRUE
OVERWRITE = TRUE
SINGLE = TRUE;

COPY INTO @~/exports/fct_crude_imports_by_grade.csv
FROM OIL_SUPPLY_CHAIN.MARTS.FCT_CRUDE_IMPORTS_BY_GRADE
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' NULL_IF = ('') COMPRESSION = NONE)
HEADER = TRUE
OVERWRITE = TRUE
SINGLE = TRUE;

COPY INTO @~/exports/fct_interregional_movements.csv
FROM OIL_SUPPLY_CHAIN.MARTS.FCT_INTERREGIONAL_MOVEMENTS
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' NULL_IF = ('') COMPRESSION = NONE)
HEADER = TRUE
OVERWRITE = TRUE
SINGLE = TRUE;  

SELECT * FROM OIL_SUPPLY_CHAIN.MARTS.FCT_SUPPLY_BALANCE;

SELECT * FROM OIL_SUPPLY_CHAIN.MARTS.FCT_GLOBAL_PRODUCTION;

SELECT * FROM OIL_SUPPLY_CHAIN.MARTS.FCT_STORAGE_CUSHING;

SELECT * FROM OIL_SUPPLY_CHAIN.MARTS.FCT_CRUDE_IMPORTS_BY_GRADE;

SELECT * FROM OIL_SUPPLY_CHAIN.MARTS.FCT_INTERREGIONAL_MOVEMENTS;

