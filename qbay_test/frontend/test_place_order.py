from seleniumbase import BaseCase
from selenium.common.exceptions import NoSuchElementException

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.users import register
from qbay.products import create_product


class PlaceOrderTest(BaseCase):
    def test_place_order(self, *_):
        # make test accounts
        assert register('Evan', 'ev@queensu.com', 'EvAnYeS21!') is True
        assert register('Ryan', 'ry@queensu.com', 'RyAnYeS21!') is True
        
        # login to first test account
        self.open(base_url + "/login")
        self.type("#email", "ev@queensu.com")
        self.type("#password", "EvAnYeS21!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # make test products
        self.open(base_url + "/product-creation")
        self.type("#product-name", "Carrot Cream Pie")
        self.type("#description", "A hot and fresh carrot cream pie, buy now!")
        self.type("#price", "10")
        self.type("#quantity", "4")
        self.click('input[type="submit"]')
        self.assert_title("Profile")
        self.open(base_url + "/product-creation")
        self.type("#product-name", "Apple Cream Pie")
        self.type("#description", "A hot and fresh macintosh apple cream pie!")
        self.type("#price", "50")
        self.type("#quantity", "10")
        self.click('input[type="submit"]')
        self.assert_title("Profile")
        self.open(base_url + "/product-creation")
        self.type("#product-name", "Pear Cream Pie")
        self.type("#description", "A hot and fresh pear cream pie!")
        self.type("#price", "1000")
        self.type("#quantity", "10")
        self.click('input[type="submit"]')
        self.assert_title("Profile")
        self.open(base_url + "/product-creation")
        self.type("#product-name", "Orange Cream Pie")
        self.type("#description", "A hot and fresh orange cream pie!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_title("Profile")

        # login to second test account
        self.open(base_url + "/login")
        self.type("#email", "ry@queensu.com")
        self.type("#password", "RyAnYeS21!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        """
        First Test Method:
        Output Coverage – sucessful or unsucessful order
        """
        # Sucessful Order Placed
        self.open(base_url + "/shop")
        self.click('input[name="Carrot Cream Pie"]')
        self.assert_title("Checkout")
        self.click('input[type="submit"]')
        self.assert_title("Shop")  # Success!

        # Unsucessful Order Placed
        self.open(base_url + "/shop")
        self.click('input[name="Carrot Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "20")
        self.click('input[type="submit"]')
        self.assert_title("Checkout")

        """
        Second Test Method:
        Input Coverage
        """

        # Balance Test: user can't place order that costs more than balance
        # Quantity Test: user can't order more than available quantity.
        # Order is successful when less than balance and available quantity
        self.open(base_url + "/shop")
        self.click('input[name="Carrot Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_title("Shop")  # Success!

        # Order is unsucessful when more than balance and available quantity
        self.open(base_url + "/shop")
        self.click('input[name="Pear Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_title("Checkout")

        # Order is successful when less than balance and valid quantity
        self.open(base_url + "/shop")
        self.click('input[name="Carrot Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_title("Shop")

        # Order is unsucessful when less than balance and invalid quantity
        self.open(base_url + "/shop")
        self.click('input[name="Carrot Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "6")
        self.click('input[type="submit"]')
        self.assert_title("Checkout")

        # Order is unsucessful when greater than balance and invalid quantity
        self.open(base_url + "/shop")
        self.click('input[name="Carrot Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "20")
        self.click('input[type="submit"]')
        self.assert_title("Checkout")

        """
        Third Test Method:
        Shotgun
        """
        # This random order should be sucessful
        self.open(base_url + "/shop")
        self.click('input[name="Orange Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_title("Shop")  # Success!

        # This random order should be unsucessful
        self.open(base_url + "/shop")
        self.click('input[name="Pear Cream Pie"]')
        self.assert_title("Checkout")
        self.type("#quantity", "2")
        self.click('input[type="submit"]')
        self.assert_title("Checkout")  # unsuccessful!

        """
        Special Case Tests:
        The following are tests for functionality and don't
        really have specific black/white box or shotgun testing
        styles. So these tests below for each requirement are
        a composition I will say these are functionality requirements
        testing. Please note for functionality testing I would like to
        reference above the blackbox and whitebox testing methods above
        (reduce duplicate tests and improve efficiency)
        which already cover the following functionalities:
        - valid quantity of purchase
        - valid balance of purchase
        - successful and unsucessful purchase
        we need to still cover the following functionalities
        - A user cannot place an order for his/her products
        - A sold product will not shown on the other user's user interface
        - A sold product can be shown on the owner's user interface
        """

        # R2: A user cannot place an order for his/her products.
        # Verify no products user made show up on buy page
        # login to first test account
        self.open(base_url + "/login")
        self.type("#email", "ev@queensu.com")
        self.type("#password", "EvAnYeS21!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")

        # Verify no Apple Cream Pie
        self.open(base_url + "/shop")
        try:
            self.click('input[name="Orange Cream Pie"]')
            # If it can click on Orange Cream Pie than this is an error
            raise ValueError('product user made can be seen in their shop')
        except NoSuchElementException:
            self.assert_title("Shop")

        # R4: A sold product will not shown on the other user's user interface
        # login back into second test account
        self.open(base_url + "/login")
        self.type("#email", "ry@queensu.com")
        self.type("#password", "RyAnYeS21!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")
        self.open(base_url + "/shop")
        self.assert_title("Shop")  # no more orange cream pies left
        try:
            self.click('input[name="Orange Cream Pie"]')
            # If it can click on Carrot Cream Pie than this is an error
            raise ValueError('non-owner can see sold out product')
        except NoSuchElementException:
            self.assert_title("Shop") 
        
        # R5: A sold product can be shown on the owner's user interface.
        # login to first test account (product owner)
        self.open(base_url + "/login")
        self.type("#email", "ev@queensu.com")
        self.type("#password", "EvAnYeS21!")
        self.click('input[type="submit"]')
        self.assert_title("Profile")
        self.click('input[name="Orange Cream Pie"]')
        # orange cream pie as we knnow from above tests is sold out
        self.assert_title("Update a Product") 
        # still present on owner's userface as can update product
        