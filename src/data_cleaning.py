import pandas as pd
import numpy as np

# Load
df = pd.read_csv("data/processed/merged_sports_data.csv")
print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Drop unnecessary columns
df.drop(columns=["Unnamed: 0", "Rank_x"], inplace=True)
print("Dropped: 'Unnamed: 0', 'Rank_x'")

# Missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# Dtypes
print("\n--- Dtypes ---")
print(df.dtypes)

# Value ranges
print("\n--- Value Range Checks ---")
range_checks = {
    "Gold":               (0, 100),
    "Silver":             (0, 100),
    "Bronze":             (0, 100),
    "Total":              (0, 300),
    "population":         (0, 2e9),
    "gdp_per_capita_usd": (0, 200_000),
    "temperature":        (-60, 40),
}
for col, (lo, hi) in range_checks.items():
    out = df[(df[col] < lo) | (df[col] > hi)]
    status = f" {len(out)} out of range" if not out.empty else "OK"
    print(f"  {col}: {status}")

# Outliers (IQR, country-level)
print("\n--- Outliers (IQR, country-level) ---")
country_df = df.drop_duplicates(subset="Country")
for col in ["Total", "population", "gdp_per_capita_usd", "temperature"]:
    Q1, Q3 = country_df[col].quantile(0.25), country_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lo, hi = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    out = country_df[(country_df[col] < lo) | (country_df[col] > hi)][["Country", col]]
    if out.empty:
        print(f"  {col}: ✓ no outliers")
    else:
        print(f"  {col}: outliers detected (kept: real-world variation)")
        print(out.to_string(index=False))

# Outliers are kept as they represent real-world variation.
# Population outliers (USA, China, Brazil) are addressed by
# using medals_per_million as a normalized metric in the analysis.

# Enrichment
print("\n--- Feature Engineering ---")

# sport_dominance_pct: percentage of a country's total medals coming from one sport
# shows how specialized a country is in a specific sport, useful for RQ5
df["sport_dominance_pct"] = (df["Sport_Total"] / df["Total"] * 100).round(2)
print("  + sport_dominance_pct")

# climate_zone: categorizes countries by average annual temperature
# Cold < 8°C, Mild 8-16°C, Warm > 16°C, useful for RQ4
bins   = [-np.inf, 8, 16, np.inf]
labels = ["Cold", "Mild", "Warm"]
df["climate_zone"] = pd.cut(df["temperature"], bins=bins, labels=labels)
print("  + climate_zone")

# Save
df.to_csv("data/processed/cleaned_sports_data.csv", index=False)
print("\n Saved: data/processed/cleaned_sports_data.csv")