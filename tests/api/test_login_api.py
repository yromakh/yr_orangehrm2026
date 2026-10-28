from typing import Any

import pytest

from utils.api_utils import ApiUtils
from utils.employee_tst import CELIA_GENISTER, EmployeeTst


api_utils: ApiUtils


@pytest.fixture(scope="module", autouse=True)
def setup_api(authenticated_context: dict[str, Any]):
    global api_utils
    api_utils = ApiUtils(authenticated_context)


@pytest.fixture(scope="module")
def employee() -> EmployeeTst:
    return CELIA_GENISTER


@pytest.mark.api
def test_login_opens_dashboard():
    dashboard_response = api_utils.open_dashboard()
    assert dashboard_response.url.endswith("/dashboard/index")


@pytest.mark.api
def test_open_pim_page():
    pim_response = api_utils.open_pim_page()
    assert pim_response.url.endswith("/pim/viewEmployeeList")

    open_pim_add_employee_response = api_utils.open_pim_add_employee_page()
    assert open_pim_add_employee_response.url.endswith("/pim/addEmployee")


@pytest.mark.api
def test_create_employee():
    pim_add_employee_response, empNumber = api_utils.save_pim_employee()
    assert pim_add_employee_response.url.endswith(
        f"/pim/viewPersonalDetails/empNumber/{empNumber}"
    )


@pytest.mark.api
def test_open_admin_page_and_add_user():
    admin_response = api_utils.open_admin_page()
    assert admin_response.url.endswith("/admin/viewSystemUsers")

    add_user_response = api_utils.open_add_user_page()
    assert add_user_response.url.endswith("/admin/saveSystemUser")
    

@pytest.mark.api
def test_load_employee_list():
    load_employee_response = api_utils.load_employee_list()
    employee_list = load_employee_response.json()["data"]
    assert len(employee_list) > 0
    

@pytest.mark.api
@pytest.mark.order(1)
@pytest.mark.dependency(name="save_employee_with_IDs_more_than_100")
def test_save_employee_using_data_from_file(employee: EmployeeTst):
    save_employee_response = api_utils.save_employee_using_file_data(employee)
    assert save_employee_response.ok


@pytest.mark.api
@pytest.mark.order(2)
@pytest.mark.dependency(depends=["save_employee_with_IDs_more_than_100"])
@pytest.mark.skip(reason="Skipping deletion of employees with IDs more than 100")
def test_delete_employees_with_IDs_more_than_100():
    deletedResponse = api_utils.delete_employees_with_IDs_more_than_100()
    assert deletedResponse is not None and deletedResponse.ok