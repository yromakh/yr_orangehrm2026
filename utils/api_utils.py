from pyexpat import model
from dataclasses import replace
from typing import Any, Dict

import csv
import json
from httperrors import BadRequestError
from pathlib import Path
import random
from playwright.sync_api import APIRequestContext, APIResponse
from utils.employee_tst import CELIA_GENISTER, EmployeeTst


class ApiUtils:
    def __init__(self, authenticated_context: dict[str, Any]):
        self.api_request_context: APIRequestContext = authenticated_context[
            "api_request_context"
        ]

    def open_dashboard(self):
        # Get dashboard
        dashboard_response: APIResponse = self.api_request_context.get(
            "dashboard/index", max_redirects=0
        )
        print("\nDASHBOARD STATUS:", dashboard_response.status)
        print("DASHBOARD URL:", dashboard_response.url)
        assert dashboard_response.ok

        return dashboard_response

    def open_admin_page(self):
        # Get admin page
        view_admin_response: APIResponse = self.api_request_context.get(
            "/web/index.php/admin/viewAdminModule", max_redirects=0
        )
        assert view_admin_response.status_text == "Found"

        view_system_users_response: APIResponse = self.api_request_context.get(
            "/web/index.php/admin/viewSystemUsers", max_redirects=0
        )
        print("\nADMIN STATUS:", view_system_users_response.status)
        print("ADMIN URL:", view_system_users_response.url)

        assert view_system_users_response.ok

        return view_system_users_response

    def open_add_user_page(self):
        # Get add user page
        add_user_response: APIResponse = self.api_request_context.get(
            "/web/index.php/admin/saveSystemUser", max_redirects=0
        )
        print("\nADD USER STATUS:", add_user_response.status)
        print("ADD USER URL:", add_user_response.url)

        assert add_user_response.ok

        return add_user_response

    def open_pim_page(self):
        # Get pim page
        view_pim_response: APIResponse = self.api_request_context.get(
            "/web/index.php/pim/viewPimModule", max_redirects=0
        )
        assert view_pim_response.status_text == "Found"

        view_employee_list_response: APIResponse = self.api_request_context.get(
            "/web/index.php/pim/viewEmployeeList", max_redirects=0
        )
        print("\nPIM page STATUS:", view_employee_list_response.status)
        print("PIM URL:", view_employee_list_response.url)

        assert view_employee_list_response.ok

        return view_employee_list_response

    def open_pim_add_employee_page(self):
        # Get Add Employee page
        add_employee_response: APIResponse = self.api_request_context.get(
            "/web/index.php/pim/addEmployee", max_redirects=0
        )
        print("\nADD EMPLOYEE page STATUS:", add_employee_response.status)
        print("ADD EMPLOYEE URL:", add_employee_response.url)
        assert add_employee_response.ok

        return add_employee_response

    def get_employees_Ids(self) -> list[str]:
        try:
            load_employee_response: APIResponse = self.api_request_context.get(
                "/web/index.php/api/v2/pim/employees", max_redirects=0
            )
            assert load_employee_response.ok
            employee_list = load_employee_response.json()["data"]
            employeeIds = [employee["employeeId"] for employee in employee_list]
            return employeeIds
        except Exception as e:
            print(f"Failed to get employee IDs: {e}")
            return []
    

    def get_new_employeeId(self, empId: str | None = None) -> str:
        employeeIds = self.get_employees_Ids()
        while True:
            if empId is not None:
                if empId not in employeeIds:
                    return empId
  
            empNumber = f"0{random.randint(100, 999)}"
            if len(employeeIds) == 0:
                return empNumber
            elif empNumber not in employeeIds:
                return empNumber

    def save_pim_employee(self) -> tuple[APIResponse, str]:
        try:
            # Save Employee data
            empNumber = self.get_new_employeeId()
        
            employee_params: Dict[str, str | float | bool] = {
                "value": empNumber,
                "entityName": "Employee",
                "attributeName": "employeeId",
            }
            # Get unique request to validate the employee data before saving
            validate_employee_response: APIResponse = self.api_request_context.get(
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

            save_employee_response: APIResponse = self.api_request_context.post(
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

            open_employee_details_response: APIResponse = self.api_request_context.get(
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
            print(
                f"BadRequestError error while reaching/creating PIM employee: {error}"
            )
            raise
        except AssertionError as error:
            print(f"Assertion error while saving PIM employee: {error}")
            raise
        except Exception as error:
            print(f"Unexpected error while saving PIM employee: {error}")
            raise

    def save_employee_using_file_data(
        self, employee: EmployeeTst = CELIA_GENISTER
    ):
        try:
            empNumber = self.get_new_employeeId(employee.employee_id)
            new_employee = replace(employee, employee_id=empNumber).to_api_payload()

            employee_params: Dict[str, str | float | bool] = {
                "value": empNumber,
                "entityName": "Employee",
                "attributeName": "employeeId",
            }
            validate_employee_response: APIResponse = self.api_request_context.get(
                "/web/index.php/api/v2/core/validation/unique", params=employee_params
            )
            if not validate_employee_response.ok:
                raise BadRequestError(
                    f"Failed to validate employee with empNumber {empNumber}. "
                    f"Status code: {validate_employee_response.status}, "
                    f"Response: {validate_employee_response.text()}"
                )
            assert validate_employee_response.ok

            save_employee_response: APIResponse = self.api_request_context.post(
                "/web/index.php/api/v2/pim/employees",
                data=new_employee,
                max_redirects=0,
                headers={"Content-Type": "application/json"},
            )

            print("\nSAVE EMPLOYEE page STATUS:", save_employee_response.status)
            if not save_employee_response.ok:
                raise BadRequestError(
                    f"Failed to save employee. "
                    f"Status code: {save_employee_response.status}, "
                    f"Response: {save_employee_response.text()}"
                )
            assert save_employee_response.ok

            return save_employee_response

        except BadRequestError as error:
            print(
                f"BadRequestError error while reaching/creating PIM employee: {error}"
            )
            raise
        except AssertionError as error:
            print(f"Assertion error while saving PIM employee: {error}")
            raise
        except Exception as error:
            print(f"Unexpected error while saving PIM employee: {error}")
            raise

    def load_employee_list(self):
        employee_params: Dict[str, str | float | bool] = {
            "limit": "50",
            "offset": "0",
            "model": "detailed",
            "includeEmployees": "onlyCurrent",
            "sortField": "employee.firstName",
            "sortOrder": "ASC"
        }
        
        load_employee_response: APIResponse = self.api_request_context.get(
            "/web/index.php/api/v2/pim/employees", params=employee_params
        )
        print("\nLOAD EMPLOYEE LIST - page STATUS:", load_employee_response.status)
        print("LOAD EMPLOYEE LIST - URL:", load_employee_response.url)
        assert load_employee_response.ok

        employee_list = load_employee_response.json()
        print(f"total: {employee_list['meta']['total']}")
        columns = [
            "empNumber",
            "lastName",
            "firstName",
            "middleName",
            "employeeId",
            "terminationId",
            "jobTitle",
            "subunit",
            "empStatus",
            "supervisors",
        ]
        output_path = (
            Path(__file__).resolve().parent.parent
            / "test_data"
            / "employee_list.csv"
        )

        with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            sorted_list = sorted(employee_list["data"], key=lambda x: x["empNumber"])
            for employee in sorted_list:
                writer.writerow(
                    {
                        column: json.dumps(employee[column], ensure_ascii=False)
                        if isinstance(employee[column], (dict, list))
                        else employee[column]
                        for column in columns
                    }
                )

        return load_employee_response

    def delete_employees_with_IDs_more_than_100(self) -> APIResponse:
        employee_response = self.load_employee_list()
        employee_data = employee_response.json()
        employees = employee_data["data"]
        total_employees = employee_data["meta"]["total"]
        page_size = 50

        for offset in range(len(employees), total_employees, page_size):
            page_response = self.api_request_context.get(
                "/web/index.php/api/v2/pim/employees",
                params={
                    "limit": str(page_size),
                    "offset": str(offset),
                    "model": "detailed",
                    "includeEmployees": "onlyCurrent",
                    "sortField": "employee.firstName",
                    "sortOrder": "ASC",
                },
            )
            assert page_response.ok
            employees.extend(page_response.json()["data"])

        # 1. retrieve list of empNumbers of employees in loop 1
        employee_ids_to_delete: list[int] = []
        for employee in employees:
            employeeId = int(employee["employeeId"])
            if employeeId > 100:
                employee_ids_to_delete.append(employeeId)

        # 2. filter employees using employee_ids_to_delete to get employees to be deleted
        employees = [employee for employee in employees if int(employee["employeeId"]) in employee_ids_to_delete]
        if len(employees) == 0:
            raise ValueError("No employees with IDs greater than 100 found.")
        
        # 3. delete employees with empNumbers greater than 100 using filtered employees
        response: APIResponse | None = None
        for employee in employees:
            emp_number = int(employee["empNumber"])
            emp_data={"ids": [emp_number]}
            response = self.api_request_context.delete(
                "/web/index.php/api/v2/pim/employees",
                data=emp_data,
            )
            print(f"Deleted employee empNumber {emp_number} - STATUS: {response.status}")
            assert response.ok, (
                f"{response.status} {response.text()}"
            )
        
        return response if response is not None else employee_response
        
