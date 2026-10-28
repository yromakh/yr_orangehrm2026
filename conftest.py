from bs4 import BeautifulSoup
import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from typing import cast
from utils.login_helper import do_credentials_exist
from pages.orange_login_page import LoginPage

load_dotenv()

ORANGEHRM_URL = os.getenv("ORANGEHRM_URL")
ORANGEHRM_USERNAME = os.getenv("ORANGEHRM_USERNAME")
ORANGEHRM_PASSWORD = os.getenv("ORANGEHRM_PASSWORD")


@pytest.fixture(scope="function")
def open_site(page: Page):
    try:
        if ORANGEHRM_URL is None:
            raise ValueError("ORANGEHRM_URL is not defined in .env file")

        if not ORANGEHRM_URL.strip():
            raise ValueError("ORANGEHRM_URL is empty in .env file")

        page.goto(ORANGEHRM_URL)
    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"Unexpected error while opening site: {error}")

    return LoginPage(page)


@pytest.fixture(scope="function")
def login_to_site(open_site):
    try:
        if do_credentials_exist(ORANGEHRM_USERNAME, ORANGEHRM_PASSWORD):
            open_site.login(cast(str, ORANGEHRM_USERNAME), cast(str, ORANGEHRM_PASSWORD))

    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"Unexpected error while logging in: {error}")


@pytest.fixture(scope="session")
def authenticated_context(playwright):

    if ORANGEHRM_URL is None:
        raise ValueError("ORANGEHRM_URL is not defined in .env file")

    if not ORANGEHRM_URL.strip():
        raise ValueError("ORANGEHRM_URL is empty in .env file")

    if not do_credentials_exist(ORANGEHRM_USERNAME, ORANGEHRM_PASSWORD):
        raise ValueError("Username or password is not defined in .env file")

    api_auth_context = playwright.request.new_context(base_url=ORANGEHRM_URL)

    # Get login page
    response = api_auth_context.get("auth/login", max_redirects=0)
    assert response.ok

    soup = BeautifulSoup(response.text(), "html.parser")
    auth_login = soup.find("auth-login")
    assert auth_login is not None, "auth-login element was not found"

    csrf_token = auth_login.get(":token")
    assert csrf_token is not None, "CSRF token was not found"

    login_response = api_auth_context.post(
        "auth/validate",
        data={
            "_token": csrf_token,
            "username": cast(str, ORANGEHRM_USERNAME),
            "password": cast(str, ORANGEHRM_PASSWORD),
        },
    )
    assert login_response.ok, "API login failed"

    yield {"csrf_token": csrf_token, "api_request_context": api_auth_context}

    api_auth_context.dispose()
