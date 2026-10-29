from playwright.sync_api import Page, expect
import pytest
from conftest import open_site
from pages.orange_home_page import HomePage
from pages.orange_login_page import LoginPage
import os
from typing import cast
from utils.login_helper import do_credentials_exist

ORANGEHRM_USERNAME = os.getenv("ORANGEHRM_USERNAME")
ORANGEHRM_PASSWORD = os.getenv("ORANGEHRM_PASSWORD")


@pytest.fixture(scope="module")
def credentials() -> tuple[str, str]:
    do_credentials_exist(ORANGEHRM_USERNAME, ORANGEHRM_PASSWORD)
    return cast(str, ORANGEHRM_USERNAME), cast(str, ORANGEHRM_PASSWORD)


def test_show_loading_brand_at_login_page(open_site: LoginPage):
    expect(open_site.loading_brand).to_be_visible()


def test_show_login_title(open_site: LoginPage):
    expect(open_site.login_heading).to_be_visible()


def test_user_is_logged_in_successfully(page: Page, open_site: LoginPage, credentials):
    home_page = HomePage(page)
    username, password = credentials
    open_site.login(cast(str, username), cast(str, password))
    expect(home_page.dashboard_label).to_be_visible(timeout=15000)


def test_show_validation_message_when_credentials_incorrect(open_site: LoginPage):
    open_site.enter_username("Admin_wrong")
    open_site.enter_password("Password_wrong123")
    open_site.click_login_button()
    expect(open_site.validation_message).to_be_visible(timeout=15000)
