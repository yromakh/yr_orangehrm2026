import pytest
from pytest_bdd import given, scenarios, then, when, parsers
from playwright.sync_api import expect
from pages.orange_home_page import HomePage
from typing import cast

scenarios("loginFeature.feature")


@pytest.fixture
def shared_data():
    return {}


@given("the user is on the login page")
def user_is_on_login_page(open_site, shared_data):
    login_page = open_site
    shared_data["login_page"] = login_page


@when(parsers.re(r"the user enters (?P<username>.*?) and (?P<password>.*)"))
def user_enters_valid_credentials(shared_data, username, password):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.enter_username(cast(str, username))
        login_page.enter_password(cast(str, password))


@when("the user clicks the login button")
def user_clicks_login_button(shared_data):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.click_login_button()
        shared_data["home_page"] = HomePage(login_page.page)


@then("the user is redirected to the dashboard page")
def user_on_dashboard_page(shared_data):
    home_page = shared_data["home_page"]
    expect(home_page.dashboard_label).to_be_visible()


@then(parsers.parse("error message is displayed {error}"))
def error_message_displayed(shared_data, error):
    login_page = shared_data["login_page"]
    expect(login_page.page.get_by_text(error, exact=True).first).to_be_visible()
