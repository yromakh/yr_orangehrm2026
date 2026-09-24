from typing import Any

import pytest

from utils.api_utils import TestApiUtils
from utils.login_helper import do_credentials_exist

@pytest.mark.api
def test_login_opens_dashboard(authenticated_context: dict[str, Any]):
    api_utils = TestApiUtils()
    dashboard_response = api_utils.open_dashboard(authenticated_context)
    assert dashboard_response.url.endswith("/dashboard/index")
    
def test_open_pim_page(authenticated_context: dict[str, Any]):
    api_utils = TestApiUtils()
    pim_response = api_utils.open_pim_page(authenticated_context)
    assert pim_response.url.endswith("/pim/viewEmployeeList")
    
    pim_add_employee_response = api_utils.open_pim_add_employee_page(authenticated_context)
    assert pim_add_employee_response.url.endswith("/pim/addEmployee")
    
    # TODO: in process
    # pim_save_employee_response = api_utils.open_pim_save_employee_page(authenticated_context)
    # assert pim_save_employee_response.url.endswith("/pim/saveEmployee")
    
def test_add_employee(authenticated_context: dict[str, Any]):
    api_utils = TestApiUtils()
    admin_response = api_utils.open_admin_page(authenticated_context)
    assert admin_response.url.endswith("/admin/viewSystemUsers")
    
    add_user_response = api_utils.open_add_user_page(authenticated_context)
    assert add_user_response.url.endswith("/admin/saveSystemUser")
    