import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from typing import cast
from utils.login_helper import do_credentials_exist
from pages.orange_login_page import LoginPage

load_dotenv()

local_URL = os.getenv("ORANGEHRM_URL")
local_user = os.getenv("ORANGEHRM_USERNAME")
local_pass = os.getenv("ORANGEHRM_PASSWORD")


@pytest.fixture(scope="function")
def open_site(page: Page):
    try:
        if local_URL is None:
            raise ValueError("ORANGEHRM_URL is not defined in .env file")

        if not local_URL.strip():
            raise ValueError("ORANGEHRM_URL is empty in .env file")

        page.goto(local_URL)
    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"Unexpected error while opening site: {error}")

    return LoginPage(page)


@pytest.fixture(scope="function")
def login_to_site(page: Page, open_site):
    try:
        if do_credentials_exist(local_user, local_pass):
            login_page = LoginPage(page)
            login_page.login(cast(str, local_user), cast(str, local_pass))

    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"Unexpected error while logging in: {error}")
