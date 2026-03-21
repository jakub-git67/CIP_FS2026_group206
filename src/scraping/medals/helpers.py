import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


def get_all_rows(driver):
    return driver.find_elements(By.XPATH, '//div[@role="row"]')


def scroll_down(driver, pixels=800, pause=0.3):
    driver.execute_script(f"window.scrollBy(0, {pixels});")
    time.sleep(pause)
    return driver.execute_script("return window.pageYOffset;")


def scroll_to_top(driver, pause=0.5):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(pause)


def parse_main_country_row(row):
    try:
        cells = row.find_elements(By.XPATH, './/div[@role="cell"]')
        values = [cell.text.strip() for cell in cells if cell.text.strip()]

        if len(values) < 6:
            return None

        rank, country, gold, silver, bronze, total = values[:6]

        return {
            "row": row,
            "Rank": rank,
            "Country": country,
            "Gold": gold,
            "Silver": silver,
            "Bronze": bronze,
            "Total": total,
        }

    except StaleElementReferenceException:
        return None