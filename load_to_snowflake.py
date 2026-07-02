import os, glob
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse="oil_supply_wh",
    database="oil_supply_chain",
    schema="raw",
)
cs = conn.cursor()

try:
    files = glob.glob("data/raw/*.json")
    print(f"Found {len(files)} files to upload.\n")

    for filepath in files:
        filename = os.path.basename(filepath).replace(".json", "")
        local_path = os.path.abspath(filepath).replace("\\", "/")

        print(f"Uploading {filename} ...")
        cs.execute(f"PUT 'file://{local_path}' @eia_stage AUTO_COMPRESS=TRUE OVERWRITE=TRUE")

        table_name = filename.upper()
        cs.execute(f"""
            CREATE OR REPLACE TABLE {table_name}_RAW (raw_json VARIANT)
        """)
        cs.execute(f"""
            COPY INTO {table_name}_RAW
            FROM @eia_stage/{filename}.json.gz
            FILE_FORMAT = json_format
            ON_ERROR = 'ABORT_STATEMENT'
        """)
        result = cs.execute(f"SELECT COUNT(*) FROM {table_name}_RAW").fetchone()
        print(f"  -> loaded {result[0]} rows into {table_name}_RAW\n")

finally:
    cs.close()
    conn.close()

print("All files loaded.")