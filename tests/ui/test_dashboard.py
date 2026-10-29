import re

from playwright.sync_api import Page, expect
import pytest
from pages.orange_home_page import HomePage


@pytest.fixture(scope="function")
def home_page(page: Page, login_to_site: None):
    return HomePage(page)


def test_dashboard_elements(home_page: HomePage):
    expect(home_page.main_menu.menu_list).to_be_visible(timeout=15000)


def test_minimize_maximize_main_menu(home_page: HomePage):
    home_page.main_menu.toggle()
    expect(home_page.orange_hrm_banner).not_to_be_visible()

    home_page.main_menu.toggle()
    expect(home_page.orange_hrm_banner).to_be_visible()


def test_main_menu_options_opening(home_page: HomePage):
    home_page.main_menu.open_admin()
    expect(home_page.admin_heading).to_be_visible()

    expect(home_page.admin_heading).to_have_text(re.compile(r"Admin *"))

    home_page.main_menu.open_pim()
    expect(home_page.pim_heading).to_have_text("PIM")


def test_update_employee_details(home_page: HomePage) -> None:
    home_page.main_menu.open_pim()
    home_page.select_employee()
    home_page.select_option(home_page.nationality_input, "Belgian")
    home_page.select_option(home_page.marital_status_input, "Married")
    home_page.license_expiry_date_input.fill("2026-10-15")
    home_page.date_of_birth_input.fill("2001-02-19")
    home_page.gender_input.click()
    home_page.save_button.click()
    expect(home_page.success_message).to_be_visible()
