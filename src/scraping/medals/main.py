import os

from browser import start_browser, close_browser
from scraper import (
    collect_country_table,
    collect_sport_table,
)


def main():
    driver = start_browser()

    try:
        country_df = collect_country_table(driver)
        country_df.to_csv("../../../data/raw/medals_country.csv", index=False, encoding="utf-8-sig")

        sport_df = collect_sport_table(driver, country_df)
        sport_df.to_csv("../../../data/raw/medals_country_sports.csv", index=False, encoding="utf-8-sig")

        print("Done.")
    finally:
        close_browser(driver)


if __name__ == "__main__":
    main()