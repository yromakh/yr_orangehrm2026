from playwright.sync_api import Page, expect


class MainMenu:
    def __init__(self, page: Page):
        self.page = page
        self.menu_list = page.locator("xpath=//ul[@class='oxd-main-menu']")
        self.toggle_button = page.locator(
            "xpath=//button[@class='oxd-icon-button oxd-main-menu-button']"
        )
        self.admin_link = page.get_by_role("link", name="Admin")
        self.pim_link = page.get_by_role("link", name="PIM")

    def toggle(self):
        self.toggle_button.click()

    def open_admin(self):
        self.admin_link.click()

    def open_pim(self):
        self.pim_link.click()
