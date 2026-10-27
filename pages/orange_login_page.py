from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.loading_brand = page.locator(".orangehrm-login-branding")
        self.login_heading = page.get_by_role("heading", name="Login")
        self.username_input = page.get_by_role("textbox", name="Username")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.validation_message = page.locator(".oxd-alert-content-text").filter(
            has_text="Invalid credentials"
        )
        self.empty_field_message = (
            page.locator(".oxd-text.oxd-text--span").filter(has_text="Required").first
        )

    def enter_username(self, username: str):
        self.username_input.fill(username)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
