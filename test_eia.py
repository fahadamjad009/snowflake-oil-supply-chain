import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("EIA_API_KEY")

# U.S. weekly crude oil stocks (excluding SPR) — a simple, well-known series for a smoke test
url = f"https://api.eia.gov/v2/seriesid/PET.WCRSTUS1.W?api_key={api_key}"

response = requests.get(url)
response.raise_for_status()
data = response.json()

print("Status code:", response.status_code)
for row in data["response"]["data"][:5]:
    print(row)