# from pages.orange_home_page import HomePage
from playwright.sync_api import Page
import re

def get_employees_count(page: Page) -> int:
    records_found = page.locator(
        ".orangehrm-horizontal-padding.orangehrm-vertical-padding"
    ).inner_text()
    match = re.search(r"\((\d+)\) Records Found", records_found)
    return int(match.group(1)) if match else 0