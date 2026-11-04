from playwright.sync_api import Locator, Page
from pages.base_page import BasePage
from pages.components.main_menu import MainMenu


class AuthenticatedPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.__main_menu = MainMenu(page)
        
    def get_menu_list(self) -> Locator:
        return self.__main_menu.menu_list

    def toggle_main_menu(self) -> None:
        self.__main_menu.toggle()

    def open_admin(self) -> None:
        self.__main_menu.open_admin()

    def open_pim(self) -> None:
        self.__main_menu.open_pim()
