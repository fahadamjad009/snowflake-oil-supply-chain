import os, json
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2"

print("=== Fix attempt: World consumption, broader query ===")
params = {"api_key": api_key, "frequency": "annual", "data[0]": "value", "length": 5,
          "facets[productId][0]": "5", "facets[activityId][0]": "2"}
r = requests.get(f"{BASE}/international/data/", params=params)
print("status:", r.status_code)
print(json.dumps(r.json(), indent=2)[:800])

print("\n=== Diagnose: crude-oil-imports 400 error ===")
params2 = {"api_key": api_key, "frequency": "monthly", "data[0]": "value", "length": 3,
           "facets[originType][0]": "CTY", "facets[destinationType][0]": "US"}
r2 = requests.get(f"{BASE}/crude-oil-imports/data/", params=params2)
print("status:", r2.status_code)
print(json.dumps(r2.json(), indent=2)[:1000])

print("\n=== crude-oil-imports metadata (check real data column name) ===")
r3 = requests.get(f"{BASE}/crude-oil-imports/", params={"api_key": api_key})
print(json.dumps(r3.json()["response"].get("data", "no data key"), indent=2))