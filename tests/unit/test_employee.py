from pathlib import Path

import pytest

from utils.employee_tst import CELIA_GENISTER, EmployeeTst, load_employees


def test_csv_loads_into_employee_object():
    employee = EmployeeTst.from_csv_file()

    assert employee.emp_picture is None
    assert employee.employee_id == "0123"
    assert employee.last_name == "Genister"
    assert employee.first_name == "Celia"
    assert employee.middle_name == "gc"


def test_default_instance_matches_csv():
    assert CELIA_GENISTER == EmployeeTst.from_csv_file()


def test_csv_with_bom_keeps_first_column_name(tmp_path: Path):
    csv_path = tmp_path / "employees.csv"
    csv_path.write_text(
        "empPicture,employeeId,lastName,firstName,middleName\nNone,0123,A,B,c\n",
        encoding="utf-8-sig",
    )

    employees = load_employees(csv_path)

    assert employees == [
        EmployeeTst(emp_picture=None, employee_id="0123", last_name="A",
                    first_name="B", middle_name="c")
    ]


def test_from_csv_row_keeps_picture_when_provided():
    row: dict[str, str | None] = {
        "empPicture": "photo.png",
        "employeeId": "0001",
        "lastName": "A",
        "firstName": "B",
        "middleName": "",
    }

    assert EmployeeTst.from_csv_row(row).emp_picture == "photo.png"


def test_from_csv_row_requires_employee_id():
    row: dict[str, str | None] = {"empPicture": "None", "employeeId": " ", "lastName": "A", "firstName": "B"}

    with pytest.raises(ValueError, match="employeeId"):
        EmployeeTst.from_csv_row(row)
