import re
from playwright.sync_api import Page, expect

class HomePage:
    
    def __init__(self, page: Page):
        self.page = page
        self.dashboard_label = page.get_by_role("heading", name="Dashboard")
        self.main_menu_list = page.locator("ul.oxd-main-menu")
        self.main_menu_button = page.locator(".oxd-icon-button.oxd-main-menu-button")
        self.orangehrm_banner = page.locator(".oxd-brand-banner")
        self.admin_menu = page.get_by_role("link", name="Admin")
        self.admin_heading = page.locator(".oxd-topbar-header-title")
        self.pim_menu = page.get_by_role("link", name="PIM")
        self.pim_heading = page.get_by_role("heading", name="PIM")        
        
    def is_dashboard_label_visible(self):
        expect(self.dashboard_label).to_be_visible()
        
    def is_main_menu_is_open(self):
        expect(self.main_menu_list).to_be_visible()
        
    def click_main_menu(self):
        self.main_menu_button.click()
        
    def click_admin_menu(self):
        self.admin_menu.click()
        
    def is_admin_heading_visible(self):
        self.click_admin_menu()
        expect(self.admin_heading).to_be_visible()
        
    def is_admin_heading_text_is_correct(self):
        expect(self.admin_heading).to_have_text(re.compile(r"Admin *"))
        
    def click_pim_menu(self):
        self.pim_menu.click()
        
    def is_pim_heading_visible(self):
        self.click_pim_menu()
        expect(self.pim_heading).to_have_text("PIM")