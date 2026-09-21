from playwright.sync_api import Page
from pages.orange_home_page import HomePage
from pages.orange_login_page import LoginPage
import os
from typing import cast
from utils.login_helper import do_credentials_exist

local_user = os.getenv("ORANGEHRM_USERNAME")  
local_pass = os.getenv("ORANGEHRM_PASSWORD")
    
def test_show_loading_brand_at_login_page(page: Page, open_site):     
    login_page = LoginPage(page)   
    login_page.display_loading_brand()
    
def test_show_login_title(page: Page, open_site):       
    login_page = LoginPage(page)
    login_page.display_login_title()

def test_user_is_logged_in_successfully(page: Page, open_site):   
    login_page = LoginPage(page)
    home_page = HomePage(page)
    
    if do_credentials_exist(local_user, local_pass):
        login_page.login(cast(str, local_user), cast(str, local_pass))
    
    home_page.is_dashboard_label_visible()

def test_show_validation_message_when_username_incorrect(page: Page, open_site):
    login_page = LoginPage(page)
    incorrect_username = "Admin_wrong"
    
    if do_credentials_exist(incorrect_username, local_pass):
        login_page.enter_username(incorrect_username)
        login_page.enter_password(cast(str, local_pass))
        
    login_page.click_login_button()
    login_page.display_validation_message()
    
def test_show_validation_message_when_password_incorrect(page: Page, open_site):
    login_page = LoginPage(page)
    incorrect_password = "Password_wrong123"
    
    if do_credentials_exist(local_user, incorrect_password):
        login_page.enter_username(cast(str, local_user))
        login_page.enter_password(incorrect_password)
    
    login_page.click_login_button()
    login_page.display_validation_message()
