import os
import pandas as pd
from scraper import fetch_gdp_per_capita
from config import OUTPUT_PATH


def main():
    # Fetch GDP per capita data from World Bank API
    df = fetch_gdp_per_capita()

    # Report missing values
    na_count = df["gdp_per_capita_usd"].isna().sum()
    print(f"Total rows fetched: {len(df)}")
    print(f"Missing GDP values: {na_count}")

    # Show countries with missing GDP values
    if na_count > 0:
        print("Countries with missing GDP:")
        print(df[df["gdp_per_capita_usd"].isna()][["country", "country_code"]].to_string())

    # Ensure output directory exists and save CSV
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()