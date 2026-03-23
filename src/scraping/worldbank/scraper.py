import requests
import pandas as pd
from config import BASE_URL, YEAR


def fetch_gdp_per_capita():
    # Set API parameters
    params = {
        "format": "json",
        "per_page": 300,
        "date": YEAR
    }

    print(f"Fetching GDP per capita data for year {YEAR}...")

    # Send request to World Bank API
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    # Validate response structure
    if len(data) < 2 or data[1] is None:
        raise ValueError("Unexpected API response structure.")

    records = data[1]

    rows = []
    for entry in records:
        # Extract relevant fields
        country = entry.get("country", {}).get("value")
        country_code = entry.get("countryiso3code")
        region = entry.get("region", {}).get("value")
        gdp_value = entry.get("value")

        rows.append({
            "country": country,
            "country_code": country_code,
            "region": region,
            "gdp_per_capita_usd": gdp_value
        })

    # Fetch valid country codes from World Bank
    country_resp = requests.get("http://api.worldbank.org/v2/country", params={
        "format": "json",
        "per_page": 300
    })
    country_data = country_resp.json()[1]

    valid_country_codes = {
        c["id"] for c in country_data
        if c["region"]["value"] != "Aggregates"
    }

    # dataframe oluştur
    df = pd.DataFrame(rows)

    # filtre uygula
    df = df[df["country_code"].isin(valid_country_codes)]

    return df