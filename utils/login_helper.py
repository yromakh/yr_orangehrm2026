"""Helper functions for login-related operations."""


def do_credentials_exist(user_name: str | None, password: str | None) -> bool:
    if user_name is None or password is None:
        raise ValueError(
            "ORANGEHRM_USERNAME or ORANGEHRM_PASSWORD is not defined in .env file"
        )

    if not user_name.strip() or not password.strip():
        raise ValueError(
            "ORANGEHRM_USERNAME or ORANGEHRM_PASSWORD is empty in .env file"
        )

    return True
