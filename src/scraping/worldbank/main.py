import os
import pandas as pd
from scraper import fetch_gdp_per_capita
from config import OUTPUT_PATH


def main():
    df = fetch_gdp_per_capita()

    # N/A report
    na_count = df["gdp_per_capita_usd"].isna().sum()
    print(f"Total rows fetched: {len(df)}")
    print(f"Missing GDP values: {na_count}")
    if na_count > 0:
        print("Countries with missing GDP:")
        print(df[df["gdp_per_capita_usd"].isna()][["country", "country_code"]].to_string())

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
