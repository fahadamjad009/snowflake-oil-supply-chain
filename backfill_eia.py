import os, json, time, re
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2"
PAGE_SIZE = 5000

with open("oil_control.json") as f:
    catalog = json.load(f)

Path("data/raw").mkdir(parents=True, exist_ok=True)

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")

for entry in catalog:
    field = entry.get("data_field", "value")
    all_rows = []
    offset = 0
    while True:
        params = {
            "api_key": api_key,
            "frequency": entry["frequency"],
            "data[0]": field,
            "length": PAGE_SIZE,
            "offset": offset,
        }
        for facet_id, values in entry["facets"].items():
            for i, v in enumerate(values):
                params[f"facets[{facet_id}][{i}]"] = v
        url = f"{BASE}/{entry['route']}/data/"
        r = requests.get(url, params=params)
        r.raise_for_status()
        payload = r.json()["response"]
        rows = payload["data"]
        all_rows.extend(rows)
        total = int(payload.get("total", len(rows)))
        print(f"[{entry['track']:<14}] {entry['label']:<45} pulled {len(all_rows)}/{total}")
        offset += PAGE_SIZE
        if len(all_rows) >= total or len(rows) == 0:
            break
        time.sleep(0.3)  # be polite to the API

    out_path = f"data/raw/{entry['track']}__{slugify(entry['label'])}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_rows, f)
    print(f"  -> saved {len(all_rows)} rows to {out_path}\n")

print("Backfill complete.")