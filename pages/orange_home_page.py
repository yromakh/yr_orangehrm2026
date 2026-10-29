import random

from playwright.sync_api import Locator, Page
import pytest
from pages.authenticated_page import AuthenticatedPage
from utils.ui_utils import get_employees_count


class HomePage(AuthenticatedPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_label = page.locator(
            "xpath=//div[contains(@class, 'oxd-topbar-header-title')]"
        )
        self.orange_hrm_banner = page.locator(".oxd-brand-banner")
        self.admin_heading = page.locator(".oxd-topbar-header-title")
        self.pim_heading = page.get_by_role("heading", name="PIM")
        self.edit_employee_icon = page.locator(
            "xpath=//i[@class='oxd-icon bi-pencil-fill']"
        )
        self.nationality_input = page.locator(
            "xpath=//label[normalize-space()='Nationality']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//i"
        )
        self.marital_status_input = page.locator(
            "xpath=//label[normalize-space()='Marital Status']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//i"
        )
        self.license_expiry_date_input = page.locator(
            "xpath=//label[normalize-space()='License Expiry Date']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )
        self.date_of_birth_input = page.locator(
            "xpath=//label[normalize-space()='Date of Birth']"
            "/ancestor::div[contains(@class,'oxd-input-group')]//input"
        )
        self.gender_input = page.get_by_text("Male", exact=True)
        self.save_button = page.locator(
            "//div[@class='orangehrm-horizontal-padding orangehrm-vertical-padding']"
            "//button[@type='submit'][normalize-space()='Save']"
        )
        self.success_message = page.get_by_text("Successfully Updated")

    def select_employee(self) -> None:
        employees_count = get_employees_count(self.page)
        assert employees_count > 0

        if employees_count <= 50:
            random_employee_index = random.randint(0, employees_count - 1)
            self.edit_employee_icon.nth(random_employee_index).click()
        elif employees_count > 50:
            random_employee_index = random.randint(0, 49)
            self.edit_employee_icon.nth(random_employee_index).click()
        else:
            pytest.skip("No employees found to select.")
        print(f"Selected employee at index: {random_employee_index}")

    def select_option(self, trigger: Locator, option_name: str) -> None:
        trigger.click()
        self.page.get_by_role("listbox").get_by_role("option", name=option_name).click()
