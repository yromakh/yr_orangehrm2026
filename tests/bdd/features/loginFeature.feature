Feature: Login to OrangeHRM
    As a user, I want to be able to log in to the OrangeHRM application

    Scenario Outline: Successful login with valid credentials
        Given the user is on the login page
        When the user enters <username> and <password>
        And the user clicks the login button
        Then the user is redirected to the dashboard page

        Examples:
            | username | password |
            | Admin    | admin123 |

    Scenario Outline: Unsuccessful login with invalid credentials
        Given the user is on the login page
        When the user enters <username> and <password>
        And the user clicks the login button
        Then error message is displayed <error>

        Examples:
            | username            | password               | error               |
            | Admin_incorrect123! | Incorrect_password123! | Invalid credentials |
            | Admin               |                        | Required            |
            |                     | admin123               | Required            |
