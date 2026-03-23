import requests
import pandas as pd
from config import BASE_URL, YEAR


def fetch_gdp_per_capita():
    params = {
        "format": "json",
        "per_page": 300,
        "date": YEAR
    }

    print(f"Fetching GDP per capita data for year {YEAR}...")
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    # World Bank API returns [metadata, results]
    if len(data) < 2 or data[1] is None:
        raise ValueError("Unexpected API response structure.")

    records = data[1]

    rows = []
    for entry in records:
        country = entry.get("country", {}).get("value")
        country_code = entry.get("countryiso3code")
        gdp_value = entry.get("value")  # None if missing

        rows.append({
            "country": country,
            "country_code": country_code,
            "gdp_per_capita_usd": gdp_value
        })

    df = pd.DataFrame(rows)
    return df
