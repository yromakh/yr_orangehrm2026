import pytest
from pytest_bdd import given, scenarios, then, when, parsers
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


@when(parsers.parse("the user enters valid {username} and {password}"))
def user_enters_valid_credentials(shared_data, username, password):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.enter_username(cast(str, username))
        login_page.enter_password(cast(str, password))


@when(parsers.parse("the user enters {invalid_username} and valid {password}"))
def user_enters_invalid_username(shared_data, invalid_username, password):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.enter_username(cast(str, invalid_username))
        login_page.enter_password(cast(str, password))


@when(parsers.parse("the user enters valid {username} and {invalid_password}"))
def user_enters_invalid_password(shared_data, username, invalid_password):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.enter_username(cast(str, username))
        login_page.enter_password(cast(str, invalid_password))


@when("the user clicks the login button")
def user_clicks_login_button(shared_data):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.click_login_button()
        shared_data["home_page"] = HomePage(login_page.page)


@then("the user is redirected to the dashboard page")
def user_on_dashboard_page(shared_data):
    home_page = shared_data["home_page"]
    if home_page:
        home_page.is_dashboard_label_visible()


@then("error message is displayed about invalid credentials")
def error_message_displayed(shared_data):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.display_validation_message()


@then("error message is displayed about empty fields")
def error_message_displayed_for_empty_fields(shared_data):
    login_page = shared_data["login_page"]
    if login_page:
        login_page.display_empty_field_message()
