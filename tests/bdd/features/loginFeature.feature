Feature: Login to OrangeHRM
    As a user, I want to be able to log in to the OrangeHRM application

    Scenario Outline: Successful login with valid credentials
        Given the user is on the login page
        When the user enters valid <username> and <password>
        And the user clicks the login button
        Then the user is redirected to the dashboard page

        Examples:
            | username | password     |
            | Admin    | UBy5^!9=)l6p |

    Scenario Outline: Unsuccessful login with invalid credentials
        Given the user is on the login page
        When the user enters <invalid_username> and valid <password>
        And the user enters valid <username> and <invalid_password>
        And the user clicks the login button
        Then error message is displayed about invalid credentials

        Examples:
            | username | password     | invalid_username    | invalid_password       |
            | Admin    | UBy5^!9=)l6p | Admin_incorrect123! | Incorrect_password123! |

    Scenario: Unsuccessful login with empty fields
        Given the user is on the login page
        When the user clicks the login button
        Then error message is displayed about empty fields