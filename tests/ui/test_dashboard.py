from playwright.sync_api import Page, expect
from pages.orange_home_page import HomePage

def test_dashboard_elements(page: Page, login_to_site):
    home_page = HomePage(page)
    home_page.is_main_menu_is_open()
    
def test_minimize_maximize_main_menu(page: Page, login_to_site):
    home_page = HomePage(page)
      
    home_page.click_main_menu()
    expect(home_page.orangehrm_banner).not_to_be_visible()
    
    home_page.click_main_menu()
    expect(home_page.orangehrm_banner).to_be_visible()
    
def test_main_menu_options_opening(page: Page, login_to_site): 
    home_page = HomePage(page)

    home_page.is_admin_heading_visible()
    home_page.is_admin_heading_text_is_correct()
    home_page.is_pim_heading_visible()