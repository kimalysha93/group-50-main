from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
from qbay.users import register


class FrontEndHomePageTest(BaseCase):
    """
    Functionality Coverage: analysis on intended actions
    Used here to ensure that the links and buttons on the homepage
    lead to the intended pages
    """

    # Logging in leads to the homepage
    def test_load_homepage(self, *_):
        # registering a new test account
        register("Park Jimin", "pjmbts@queensu.ca", "Apple123!")

        self.open(base_url + '/login')
        self.type("#email", "pjmbts@queensu.ca")
        self.type("#password", "Apple123!")
        self.click('input[type="submit"]')

        self.assert_element("#welcome-header")
        self.assert_text("Welcome Park Jimin!", "#welcome-header")

    # Product Creation link leads to Product Creation page
    def test_load_product_creation(self, *_):
        # logging into test account
        self.open(base_url + '/login')
        self.type("#email", "pjmbts@queensu.ca")
        self.type("#password", "Apple123!")
        self.click('input[type="submit"]')

        self.click('a[href="/product-creation"]')
        self.assert_title("Create a Product")

        # Home link on Product Creation Page leads to Home page
        self.click('a[href="/"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Park Jimin!", "#welcome-header")

    # Update Profile link leads to Update Profile page
    def test_load_update_profile(self, *_):
        # logging into test account
        self.open(base_url + '/login')
        self.type("#email", "pjmbts@queensu.ca")
        self.type("#password", "Apple123!")
        self.click('input[type="submit"]')

        self.click('a[href="/update-profile"]')
        self.assert_title("Update Profile")

        # Home link on Updatee Profile Page leads to Home page
        self.click('a[href="/"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Park Jimin!", "#welcome-header")

    # Update Product link leads to Update Product page
    def test_load_update_product(self, *_):
        # logging into test account
        self.open(base_url + '/login')
        self.type("#email", "pjmbts@queensu.ca")
        self.type("#password", "Apple123!")
        self.click('input[type="submit"]')

        # creating new product
        self.click('a[href="/product-creation"]')
        self.type("#product-name", "Chimmy Doll")
        self.type("#description", "BT21 Merchandise for BTS Jimin")
        self.type("#price", "95")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')

        # checking Update Product button on homepage
        self.click('input[name="Chimmy Doll"]')
        self.assert_title("Update a Product")

        # Home link on Updatee Profile Page leads to Home page
        self.click('a[href="/"]')
        self.assert_element("#welcome-header")
        self.assert_text("Welcome Park Jimin!", "#welcome-header")

    # Log out link leads to the Log In page
    def test_load_logout(self, *_):
        self.open(base_url + '/login')
        self.type("#email", "pjmbts@queensu.ca")
        self.type("#password", "Apple123!")
        self.click('input[type="submit"]')

        self.click('a[href="/logout"]')
        self.assert_title("Log In")
