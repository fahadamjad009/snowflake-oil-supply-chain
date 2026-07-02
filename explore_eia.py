import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2"

def show_routes(path, depth=0):
    url = f"{BASE}/{path}?api_key={api_key}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()["response"]
    indent = "  " * depth
    if "routes" in data:
        for route in data["routes"]:
            print(f"{indent}{path}/{route['id']:<20} {route['name']}")
        return data["routes"]
    else:
        print(f"{indent}{path} -> DATA ROUTE (frequencies: {[f['id'] for f in data.get('frequency', [])]})")
        return []

print("=== PETROLEUM ===")
petro_routes = show_routes("petroleum")
for r in petro_routes:
    show_routes(f"petroleum/{r['id']}", depth=1)

print("\n=== INTERNATIONAL ===")
show_routes("international")

print("\n=== CRUDE OIL IMPORTS ===")
show_routes("crude-oil-imports")