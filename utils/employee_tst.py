import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EMPLOYEE_CSV_PATH = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "employee_list_new_employee.csv"
)

_REQUIRED_COLUMNS = ("employeeId", "lastName", "firstName")
_NO_PICTURE_VALUES = ("", "none", "null")


@dataclass
class EmployeeTst:
    employee_id: str
    last_name: str
    first_name: str
    middle_name: str = ""
    emp_picture: str | None = None

    @classmethod
    def from_csv_row(cls, row: dict[str, str | None]) -> "EmployeeTst":
        for column in _REQUIRED_COLUMNS:
            value = row.get(column)
            if not value or not value.strip():
                raise ValueError(f"Employee CSV requires a value for {column}")

        picture = (row.get("empPicture") or "").strip()
        return cls(
            emp_picture=None if picture.lower() in _NO_PICTURE_VALUES else picture,
            employee_id=(row["employeeId"] or "").strip(),
            last_name=(row["lastName"] or "").strip(),
            first_name=(row["firstName"] or "").strip(),
            middle_name=(row.get("middleName") or "").strip(),
        )

    @classmethod
    def from_csv_file(cls, path: Path = EMPLOYEE_CSV_PATH) -> "EmployeeTst":
        return load_employees(path)[0]

    def to_api_payload(self) -> dict[str, Any]:
        return {
            "empPicture": self.emp_picture,
            "employeeId": self.employee_id,
            "lastName": self.last_name,
            "firstName": self.first_name,
            "middleName": self.middle_name,
        }


def load_employees(path: Path = EMPLOYEE_CSV_PATH) -> list[EmployeeTst]:
    columns = ["empPicture", "employeeId", "lastName", "firstName", "middleName"]
    # utf-8-sig strips the BOM so the first column name is not corrupted.
    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or not set(columns).issubset(reader.fieldnames):
            raise ValueError(f"Employee CSV must contain columns: {columns}")
        employees = [EmployeeTst.from_csv_row(row) for row in reader]

    if not employees:
        raise ValueError(f"Employee CSV contains no employee data: {path}")
    return employees


CELIA_GENISTER = EmployeeTst.from_csv_file()
