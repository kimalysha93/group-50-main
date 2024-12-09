"""
Testing file for products.py
"""

# Import the required functions for testing
from qbay.transactions import order_product
from qbay.users import (get_balance, register, increase_balance,
                        decrease_balance)
from qbay.products import create_product
from qbay_test.test_products import valid_description

# Define any required variables for testing
seller = "orientation@compsa.queensu.ca"
buyer = "tc_fundraising@compsa.queensu.ca"
product1 = "Banana Cream Pie"
product2 = "Windows 98 V123456"
product3 = "IKEA Table Brown"
product4 = "XBOX 1XS SLIM MICRO DAY1 ED"
product5 = "10 Dollar Pie"
product6 = "Another 10 Dollar Pie"


def test_r6_1_transaction():
    """
    Testing R6-1: A user can place an order on the products.
    """

    # Create two users and some sample products for testing
    register("High Tech Truman", seller, "Truwu4321!")  # Make products
    register("Best TC Role", buyer, "CallieHype1234!")  # Buy products

    # Give our users some money to buy products
    increase_balance(buyer, 1000000)
    increase_balance(seller, 1000000)

    # Create some products to purchase for testing
    create_product(product1, valid_description, 1000, seller)
    create_product(product2, valid_description, 5000, seller, quantity=10)

    # Test transactions
    assert order_product(product1, 1, buyer, seller) is True
    assert order_product(product2, 1, buyer, seller) is True

    # Test that quantities are valid
    assert order_product(product1, 1, buyer, seller) is False
    assert order_product(product2, 1, buyer, seller) is True
    assert order_product(product2, 9, buyer, seller) is False
    assert order_product(product2, 8, buyer, seller) is True


def test_r6_2_transaction():
    """
    Testing R6-2: A user cannot place an order for his/her products.
    """

    # Test using users from the previous test case
    create_product(product3, valid_description, 7500, seller)
    assert order_product(product3, 1, seller, seller) is False

    create_product(product4, valid_description, 60000, buyer)
    assert order_product(product4, 1, buyer, buyer) is False


def test_r6_3_transaction():
    """
    Testing R6-3: A user cannot place an order that costs more than his/her
                  balance.
    """

    # Set the buyer to have $9.99
    decrease_balance(buyer, get_balance(buyer) - 999)

    # Create test products
    create_product(product5, valid_description, 1000, seller)
    create_product(product6, valid_description, 1000, seller)

    # 1cent short of price
    assert order_product(product5, 1, buyer, seller) is False

    # Give the 1cent and try again
    increase_balance(buyer, 1)
    assert order_product(product5, 1, buyer, seller) is True

    # Test that the balance was adjusted (attempt to purchase another product)
    assert order_product(product6, 1, buyer, seller) is False

    # Give $10 then try to buy again
    increase_balance(buyer, 1000)
    assert order_product(product6, 1, buyer, seller) is True
