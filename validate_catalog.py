import os, json
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2"

with open("oil_control.json") as f:
    catalog = json.load(f)

for entry in catalog:
    field = entry.get("data_field", "value")
    params = {"api_key": api_key, "frequency": entry["frequency"], "data[0]": field, "length": 3}
    for facet_id, values in entry["facets"].items():
        for i, v in enumerate(values):
            params[f"facets[{facet_id}][{i}]"] = v
    url = f"{BASE}/{entry['route']}/data/"
    r = requests.get(url, params=params)
    status = r.status_code
    n = len(r.json()["response"]["data"]) if status == 200 else 0
    print(f"[{entry['track']:<14}] {entry['label']:<45} status={status} rows={n}")
    if status != 200:
        print("    ERROR:", r.json())
    elif n > 0:
        print("    sample:", r.json()["response"]["data"][0])