from typing import Dict

from httperrors import BadRequestError
import os
import random
import time
from playwright.sync_api import APIRequestContext, APIResponse, sync_playwright

local_URL = os.getenv("ORANGEHRM_URL")
username = os.getenv("ORANGEHRM_USERNAME")
password = os.getenv("ORANGEHRM_PASSWORD")


class TestApiUtils:

    def login(self, authenticated_context):
        csrf_token = authenticated_context["csrf_token"]
        api_request_context = authenticated_context["api_request_context"]

        login_credentials = {
            "_token": csrf_token,
            "username": username,
            "password": password,
        }

        # Perform authentication request / Login API call
        response = api_request_context.post("auth/validate", data=login_credentials)
        assert response.ok

    def open_dashboard(self, authenticated_context):
        self.login(authenticated_context)
        api_request_context = authenticated_context["api_request_context"]

        # Get dashboard
        dashboard_response: APIResponse = api_request_context.get(
            "dashboard/index", max_redirects=0
        )
        print("\nDASHBOARD STATUS:", dashboard_response.status)
        print("DASHBOARD URL:", dashboard_response.url)
        assert dashboard_response.ok

        return dashboard_response

    def open_admin_page(self, authenticated_context):
        self.login(authenticated_context)

        api_request_context: APIRequestContext = authenticated_context[
            "api_request_context"
        ]

        # Get admin page
        view_admin_response: APIResponse = api_request_context.get(
            "/web/index.php/admin/viewAdminModule", max_redirects=0
        )
        assert view_admin_response.status_text == "Found"

        view_system_users_response: APIResponse = api_request_context.get(
            "/web/index.php/admin/viewSystemUsers", max_redirects=0
        )
        print("\nADMIN STATUS:", view_system_users_response.status)
        print("ADMIN URL:", view_system_users_response.url)

        assert view_system_users_response.ok

        return view_system_users_response

    def open_add_user_page(self, authenticated_context):
        self.login(authenticated_context)

        api_request_context: APIRequestContext = authenticated_context[
            "api_request_context"
        ]

        # Get add user page
        add_user_response: APIResponse = api_request_context.get(
            "/web/index.php/admin/saveSystemUser", max_redirects=0
        )
        print("\nADD USER STATUS:", add_user_response.status)
        print("ADD USER URL:", add_user_response.url)

        assert add_user_response.ok

        return add_user_response

    def open_pim_page(self, authenticated_context):
        self.login(authenticated_context)

        api_request_context: APIRequestContext = authenticated_context[
            "api_request_context"
        ]

        # Get pim page
        view_pim_response: APIResponse = api_request_context.get(
            "/web/index.php/pim/viewPimModule", max_redirects=0
        )
        assert view_pim_response.status_text == "Found"

        view_employee_list_response: APIResponse = api_request_context.get(
            "/web/index.php/pim/viewEmployeeList", max_redirects=0
        )
        print("\nPIM page STATUS:", view_employee_list_response.status)
        print("PIM URL:", view_employee_list_response.url)

        assert view_employee_list_response.ok

        return view_employee_list_response

    def open_pim_add_employee_page(self, authenticated_context):
        self.login(authenticated_context)

        api_request_context: APIRequestContext = authenticated_context[
            "api_request_context"
        ]

        # Get Add Employee page
        add_employee_response: APIResponse = api_request_context.get(
            "/web/index.php/pim/addEmployee", max_redirects=0
        )
        print("\nADD EMPLOYEE page STATUS:", add_employee_response.status)
        print("ADD EMPLOYEE URL:", add_employee_response.url)
        assert add_employee_response.ok

        return add_employee_response


    def save_pim_employee(self, authenticated_context) -> tuple[APIResponse, str]:
        try:
            self.login(authenticated_context)

            api_request_context: APIRequestContext = authenticated_context[
                "api_request_context"
            ]

            # Save Employee data
            empNumber = f"0{random.randint(100, 999)}"
            # empNumber = "0015"
            employee_params: Dict[str, str | float | bool] = {
                "value": empNumber,
                "entityName": "Employee",
                "attributeName": "employeeId",
            }
            # Get unique request to validate the employee data before saving
            validate_employee_response: APIResponse = api_request_context.get(
                "/web/index.php/api/v2/core/validation/unique", params=employee_params
            )
            if not validate_employee_response.ok:
                raise BadRequestError(
                    f"Failed to validate employee with empNumber {empNumber}. "
                    f"Status code: {validate_employee_response.status}, "
                    f"Response: {validate_employee_response.text()}"
                )
            assert validate_employee_response.ok

            # Post save employee page
            new_employee = {
                "empPicture": None,
                "employeeId": empNumber,
                "lastName": "Wallas15",
                "firstName": "William15",
                "middleName": "bb",
            }

            save_employee_response: APIResponse = api_request_context.post(
                "/web/index.php/api/v2/pim/employees",
                data=new_employee,
                max_redirects=0,
                headers={"Content-Type": "application/json"},
            )

            print("\nSAVE EMPLOYEE page STATUS:", save_employee_response.status)
            if not save_employee_response.ok:
                raise BadRequestError(
                    f"Failed to save employee with empNumber {empNumber}. "
                    f"Status code: {save_employee_response.status}, "
                    f"Response: {save_employee_response.text()}"
                )
            assert save_employee_response.ok
            # empNumber = save_employee_response.json()["data"]["empNumber"]

            open_employee_details_response: APIResponse = api_request_context.get(
                f"/web/index.php/pim/viewPersonalDetails/empNumber/{empNumber}",
                max_redirects=0,
            )
            print(
                "\nEMPLOYEE DETAILS page STATUS:", open_employee_details_response.status
            )
            if not open_employee_details_response.ok:
                raise BadRequestError(
                    f"Failed to open employee details page for empNumber {empNumber}. "
                    f"Status code: {open_employee_details_response.status}, "
                    f"Response: {open_employee_details_response.text()}"
                )
            assert open_employee_details_response.ok

            return open_employee_details_response, empNumber
        
        except BadRequestError as error:
            print(f"BadRequestError error while reaching/creating PIM employee: {error}")
            raise
        except AssertionError as error:
            print(f"Assertion error while saving PIM employee: {error}")
            raise
        except Exception as error:
            print(f"Unexpected error while saving PIM employee: {error}")
            raise
