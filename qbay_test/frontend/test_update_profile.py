from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
from qbay.users import register


"""
Black Box Methods Used:
- Shotgun Testing: choosing random input values
- Input Coverage: analysis on the intended inputs
- Output Coverage: analysis on the intended outputs
"""


class FrontUpdateProfilePageTest(BaseCase):

    """
    R3-1: A user is only able to update:
    - user name
    - shipping_address
    - postal_code
    """
    def test_update_profile_r3_1_user_name(self, *_):
        """
        R3-4: User name follows the requirements in R1 (listed below).

        R1-5: User name has to be non-empty, alphanumeric-only,
                and space allowed only if it is not as the prefix or suffix.
        R1-6: User name has to be longer than 2 characters and
                less than 20 characters.
        """
        # registering and logging into a new test account

        register("Goro Akechi", "detectiveprince@queensu.ca", "P3r5on4!!")
        self.open(base_url + '/login')
        self.type("#email", "detectiveprince@queensu.ca")
        self.type("#password", "P3r5on4!!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Goro Akechi!", "#welcome-header")

        self.click('a[href="/update-profile"]')
        self.assert_title("Update Profile")

        # Output Partition Testing

        # username is updated - valid input
        self.type("#name", "Robin Hood")
        self.click('input[value="Update Username"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Robin Hood!", "#welcome-header")

        # username is not updated - invalid input
        self.open(base_url + '/update-profile')
        self.type("#name", "")
        self.click('input[value="Update Username"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Username", "#message")

        # Shotgun Partition Testing

        # invalid - not alphanumeric and not longer than 2 characters
        self.open(base_url + '/update-profile')
        self.type("#name", ":)")
        self.click('input[value="Update Username"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Username", "#message")

        # invalid - not alphanumeric and longer than 20 characters
        self.open(base_url + '/update-profile')
        self.type("#name", "My skills exceed yours!")
        self.click('input[value="Update Username"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Username", "#message")

        # invalid - space in prefix
        self.open(base_url + '/update-profile')
        self.type("#name", " uwu owo")
        self.click('input[value="Update Username"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Username", "#message")

        # invalid - space in suffix
        self.open(base_url + '/update-profile')
        self.type("#name", "Coffee Bean ")
        self.click('input[value="Update Username"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Username", "#message")

        # valid
        self.open(base_url + '/update-profile')
        self.type("#name", "No 1 Ace Detective")
        self.click('input[value="Update Username"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome No 1 Ace Detective!", "#welcome-header")

    def test_update_profile_r3_1_shipping_address(self, *_):
        """
        R3-2: Shipping_address should be non-empty, alphanumeric-only,
                and no special characters such as !.
        """

        # registering and logging into a new test account
        register("Karma Akabane", "redhairdontcare@queensu.ca", "C0mb4t!")

        self.open(base_url + '/login')
        self.type("#email", "redhairdontcare@queensu.ca")
        self.type("#password", "C0mb4t!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Karma Akabane!", "#welcome-header")

        self.click('a[href="/update-profile"]')
        self.assert_title("Update Profile")

        # Input Partition Testing

        # valid - non-empty and only alphanumeric
        #         no special characters
        self.type("#shipping_address", "365 Days Left")
        self.click('input[value="Update Shipping Address"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Karma Akabane!", "#welcome-header")

        # invalid - not non-empty
        self.open(base_url + '/update-profile')
        self.type("#shipping_address", "")
        self.click('input[value="Update Shipping Address"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Shipping Address", "#message")

        # invalid - not alphanumeric & contains special characters
        self.open(base_url + '/update-profile')
        self.type("#shipping_address", "owo fix my code!")
        self.click('input[value="Update Shipping Address"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Shipping Address", "#message")

        # invalid - not non-empty with no alphanumeric & contains
        #           special characters is not a possible input

        # Output Partion Testing

        # shipping address is updated - valid input
        self.open(base_url + '/update-profile')
        self.type("#shipping_address", "Class 3E")
        self.click('input[value="Update Shipping Address"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Karma Akabane!", "#welcome-header")

        # shipping address is not updated - invalid input
        self.open(base_url + '/update-profile')
        self.type("#shipping_address", "Octopus?!")
        self.click('input[value="Update Shipping Address"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Shipping Address", "#message")

    def test_update_profile_r3_1_postal_code(self, *_):
        """
        R3-3: Postal code has to be a valid Canadian postal code.
        """
        # registering and logging into a new test account
        register("Noriaki Kakyoin", "hierophantgreen@queensu.ca",
                 "EmeraldSp1ash!")

        self.open(base_url + '/login')
        self.type("#email", "hierophantgreen@queensu.ca")
        self.type("#password", "EmeraldSp1ash!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Noriaki Kakyoin!", "#welcome-header")

        self.click('a[href="/update-profile"]')
        self.assert_title("Update Profile")

        # Input Testing
        # valid Canadian postal code
        self.type("#postal_code", "F2E 1B2")
        self.click('input[value="Update Postal Code"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Noriaki Kakyoin!", "#welcome-header")

        # invalid Canadian postal code
        self.open(base_url + '/update-profile')
        self.type("#postal_code", "THE FEELS by TWICE")
        self.click('input[value="Update Postal Code"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Postal Code", "#message")

        # Output Testing
        # postal code is accepted
        self.open(base_url + '/update-profile')
        self.type("#postal_code", "J0J 0P3")
        self.click('input[value="Update Postal Code"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Noriaki Kakyoin!", "#welcome-header")

        # postal code is rejected
        self.open(base_url + '/update-profile')
        self.type("#postal_code", "THE WORLD")
        self.click('input[value="Update Postal Code"]')
        self.assert_title("Update Profile")
        self.assert_text("Failed to Update Postal Code", "#message")
