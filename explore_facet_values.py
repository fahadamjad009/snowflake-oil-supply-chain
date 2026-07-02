import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2"
Path("facets").mkdir(exist_ok=True)

def get_facet_values(route, facet_id):
    url = f"{BASE}/{route}/facet/{facet_id}?api_key={api_key}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()["response"]["facets"]

def dump_and_summarize(route, facet_id, keyword_filter=None, max_print=20):
    safe_route = route.replace("/", "_")
    values = get_facet_values(route, facet_id)
    fname = f"facets/{safe_route}__{facet_id}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(values, f, indent=2)
    print(f"\n[{route} / {facet_id}]  total={len(values)}  saved -> {fname}")
    shown = values
    if keyword_filter:
        shown = [v for v in values if any(k.lower() in str(v.get("name", "")).lower() for k in keyword_filter)]
        print(f"  filtered matches for {keyword_filter}:")
    for v in shown[:max_print]:
        print(f"  {v.get('id'):<15} {v.get('name')}")

print("=== INTERNATIONAL ===")
dump_and_summarize("international", "productId")
dump_and_summarize("international", "activityId")
dump_and_summarize("international", "countryRegionId",
    keyword_filter=["United States", "Saudi Arabia", "Russia", "China", "Iraq", "Iran",
                     "Canada", "Kuwait", "Nigeria", "Brazil", "Venezuela",
                     "United Arab Emirates", "World"])

print("\n=== CRUDE OIL IMPORTS ===")
dump_and_summarize("crude-oil-imports", "originType")
dump_and_summarize("crude-oil-imports", "destinationType")
dump_and_summarize("crude-oil-imports", "gradeId")
dump_and_summarize("crude-oil-imports", "originId",
    keyword_filter=["Saudi Arabia", "Canada", "Mexico", "Russia", "Nigeria", "Iraq", "Colombia", "Ecuador", "Brazil"])

print("\n=== PETROLEUM SUB-ROUTES (duoarea / product / series) ===")
routes_keywords = {
    "petroleum/stoc/wstk": ["Cushing", "Crude Oil", "Ending Stocks", "SPR"],
    "petroleum/stoc/cu": ["Cushing", "Crude Oil"],
    "petroleum/move/impcus": ["Crude Oil", "Total"],
    "petroleum/move/ptb": ["Crude Oil", "Pipeline", "Tanker"],
    "petroleum/pnp/unc": ["Utilization", "Operable", "Gross Inputs"],
    "petroleum/sum/snd": ["Crude Oil", "Ending Stocks", "Production", "Imports", "Exports"],
}
for route, kws in routes_keywords.items():
    dump_and_summarize(route, "duoarea")
    dump_and_summarize(route, "product")
    dump_and_summarize(route, "series", keyword_filter=kws)