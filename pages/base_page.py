from playwright.sync_api import Page
from pages.components.main_menu import MainMenu


class BasePage:
    def __init__(self, page: Page):
        self.page = page
