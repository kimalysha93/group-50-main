from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
from qbay.users import register

"""
This file defines all integration tests for the frontend homepage.
"""


class FrontEndLoginAndRegistrationPageTest(BaseCase):
    def test_login(self, *_):
        """
        Output Coverage – analysis of intended outputs
        1. unsucessful registration where output is False
        so it stays on the registration page with the expected
        message of "Registration failed."
        2. sucessful registration where output is True so it
        switches to the login page with the expected message of
        "Please login"
        """

        assert register('test99', 'test101@test.com', 'Correct123!') is True

        # 1. unsucessful login
        self.open(base_url + '/login')
        self.type("#email", "test101@test.com")
        self.type("#password", "Correct12!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 2. sucessful login
        self.open(base_url + '/login')
        self.type("#email", "test101@test.com")
        self.type("#password", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")

        """
        Input Coverage - analysis of intended inputs
        """
        # 1. Invalid email (not in database), Invalid password
        self.open(base_url + '/login')
        self.type("#email", "bruh@test.com")
        self.type("#password", "correct12!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 2. valid email, invalid password
        self.open(base_url + '/login')
        self.type("#email", "test101@test.com")
        self.type("#password", "Correct12!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 3. Invalid email, valid password
        self.open(base_url + '/login')
        self.type("#email", "bruh@test.com")
        self.type("#password", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 4. valid email, valid password
        self.open(base_url + '/login')
        self.type("#email", "test101@test.com")
        self.type("#password", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")

        """
        functionality coverage – analysis on intended actions
        R1-3: The email has to follow addr-spec defined in RFC 5322
        (see https://en.wikipedia.org/wiki/Email_address for a human-
        friendly explanation). You can use external libraries/imports.
        R1-4: Password has to meet the required complexity: minimum
        length 6, at least one upper case, at least one lower case,
        and at least one special character.
        """
        # 1. Invalid RFC 5322 email
        self.open(base_url + '/login')
        self.type("#email", "test3002test.com")
        self.type("#password", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Log In", "#page-name")
        # special assert as email missing @ won't allow submit

        # 2. Password length less than 6
        self.open(base_url + '/login')
        self.type("#email", "test3002@test.com")
        self.type("#password", "Co12!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 3. Password no uppercase
        self.open(base_url + '/login')
        self.type("#email", "test3002@test.com")
        self.type("#password", "correct123!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 4. Password no lowercase
        self.open(base_url + '/login')
        self.type("#email", "test3002@test.com")
        self.type("#password", "CORRECT123!")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

        # 5. Password no special character
        self.open(base_url + '/login')
        self.type("#email", "test3002@test.com")
        self.type("#password", "Correct123")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

    def test_register(self, *_):
        """
        Output Coverage – analysis of intended outputs
        1. unsucessful registration where output is False
        so it stays on the registration page with the expected
        message of "Registration failed."
        2. sucessful registration where output is True so it
        switches to the login page with the expected message of
        "Please login"
        """

        # 1. output is False (invalid password)
        self.open(base_url + '/register')
        self.type("#email", "test211@test.com")
        self.type("#name", "testUser01")
        self.type("#password", "123456")
        self.type("#password2", "123456")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 2. output is True (valid email, username and password)
        self.open(base_url + '/register')
        self.type("#email", "test211@test.com")
        self.type("#name", "testUser01")
        self.type("#password", "Password123!")
        self.type("#password2", "Password123!")
        self.click('input[type="submit"]')
        self.assert_text("Please login", "#message")

        """
        Input Coverage - analysis of intended inputs
        """

        # 1. Invalid email, Invalid password, Passwords don't match
        self.open(base_url + '/register')
        self.type("#email", "test")
        self.type("#name", "testUser1")
        self.type("#password", "123456")
        self.type("#password2", "1234567")
        self.click('input[type="submit"]')
        self.assert_text("Register", "#page-name")

        # 2. Valid email, Invalid password, Passwords don't match
        self.open(base_url + '/register')
        self.type("#email", "test3001@test.com")
        self.type("#name", "testUser1")
        self.type("#password", "123456")
        self.type("#password2", "1234567")
        self.click('input[type="submit"]')
        self.assert_text("Register", "#page-name")

        # 3. Invalid email, Valid password, Passwords don't match
        self.open(base_url + '/register')
        self.type("#email", "test")
        self.type("#name", "testUser1")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct1!")
        self.click('input[type="submit"]')
        self.assert_text("Register", "#page-name")

        # 4. Invalid email, Invalid password, Passwords match
        self.open(base_url + '/register')
        self.type("#email", "test")
        self.type("#name", "testUser1")
        self.type("#password", "123456")
        self.type("#password2", "123456")
        self.click('input[type="submit"]')
        self.assert_text("Register", "#page-name")

        # 5. Valid email, Valid password, Passwords don't match
        self.open(base_url + '/register')
        self.type("#email", "test3001@test.com")
        self.type("#name", "testUser1")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct1!")
        self.click('input[type="submit"]')
        self.assert_text("The passwords do not match", "#message")

        # 6. Valid email, Invalid password, Passwords match
        self.open(base_url + '/register')
        self.type("#email", "1@test.com")
        self.type("#name", "testUser1")
        self.type("#password", "123456")
        self.type("#password2", "123456")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 7. Invalid email, Valid password, Passwords match
        self.open(base_url + '/register')
        self.type("#email", "test")
        self.type("#name", "testUser1")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Register", "#page-name")

        # 8. Valid email, Valid password, Passwords match
        self.open(base_url + '/register')
        self.type("#email", "test3001@test.com")
        self.type("#name", "testUser1")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Please login", "#message")

        """
        functionality coverage – analysis on intended actions
        R1-3: The email has to follow addr-spec defined in RFC
        5322 (see https://en.wikipedia.org/wiki/Email_address
        for a human-friendly explanation). You can use external
        libraries/imports.
        R1-4: Password has to meet the required complexity:
        minimum length 6, at least one upper case, at least one
        lower case, and at least one special character.
        R1-5: User name has to be non-empty, alphanumeric-only,
        and space allowed only if it is not as the prefix or
        suffix.
        R1-6: User name has to be longer than 2 characters and
        less than 20 characters.
        R1-7: If the email has been used, the operation failed.
        """
        # 1. Invalid RFC 5322 email
        self.open(base_url + '/register')
        self.type("#email", "test3002test.com")
        self.type("#name", "testUser2")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Register", "#page-name")
        # special assert as email missing @ won't allow submit

        # 2. Password length less than 6
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser2")
        self.type("#password", "Co12!")
        self.type("#password2", "Co12!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 3. Password no uppercase
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser2")
        self.type("#password", "correct123!")
        self.type("#password2", "correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 4. Password no lowercase
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser2")
        self.type("#password", "CORRECT123!")
        self.type("#password2", "CORRECT123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 5. Password no special character
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser2")
        self.type("#password", "Correct123")
        self.type("#password2", "Correct123")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 6. Username empty - can't test with selenium as won't submit
        """
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")
        """

        # 7. Username has non-alphanumeric
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser2!")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 8. Username prefix space
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", " testUser2")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 9. Username suffix space
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser ")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 10. Username less than 2 characters
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "t")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 11. Username greater than 20 characters
        self.open(base_url + '/register')
        self.type("#email", "test3002@test.com")
        self.type("#name", "testUser10000000000000000000")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")

        # 12. Email already registered
        self.open(base_url + '/register')
        self.type("#email", "test3001@test.com")
        self.type("#name", "testUser30")
        self.type("#password", "Correct123!")
        self.type("#password2", "Correct123!")
        self.click('input[type="submit"]')
        self.assert_text("Registration failed.", "#message")
