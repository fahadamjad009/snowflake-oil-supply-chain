import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2"

def show_facets(path):
    url = f"{BASE}/{path}?api_key={api_key}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()["response"]
    print(f"\n--- {path} ---")
    print("Frequencies:", [f["id"] for f in data.get("frequency", [])])
    print("Facets:")
    for facet in data.get("facets", []):
        print(f"  {facet['id']:<15} {facet['description']}")
    print("Start/End:", data.get("startPeriod"), "to", data.get("endPeriod"))

for route in [
    "international",
    "crude-oil-imports",
    "petroleum/stoc/wstk",
    "petroleum/stoc/cu",
    "petroleum/move/impcus",
    "petroleum/move/ptb",
    "petroleum/pnp/unc",
    "petroleum/sum/snd",
]:
    show_facets(route)