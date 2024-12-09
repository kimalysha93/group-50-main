"""
Testing file for products.py
"""

import datetime
from qbay.users import find_user, register
from qbay.products import (create_product, get_product,
                           update_product_description, update_product_price,
                           update_product_quantity, update_product_title)
# Define any required variables for testing
valid_description = ("Lorem ipsum dolor sit amet, consectetur "
                     "adipiscing elit. Sed accumsan imperdiet "
                     "cursus.")
valid_price = 1000
valid_email = "test0@queensu.ca"


def test_r4_1_product():
    """
    Testing R4-1: The title of the product has to be
      alphanumeric-only, and space allowed only if it is not as
      prefix and suffix.
    """

    # Create a user for testing
    register("Stephen Strange", valid_email, "Dormama24h!!")

    assert create_product("Apple Pie", valid_description,
                          valid_price, valid_email) is True
    assert create_product(" Berry Pie", valid_description,
                          valid_price, valid_email) is False
    assert create_product("Pear Pie ", valid_description,
                          valid_price, valid_email) is False
    assert create_product("Pie-Pie", valid_description,
                          valid_price, valid_email) is False
    assert create_product("Strawberry Pie 98", valid_description,
                          valid_price, valid_email) is True
    assert create_product("0123456789", valid_description,
                          valid_price, valid_email) is True


def test_r4_2_product():
    """
    Testing R4-2: The title of the product is no longer than 80
      characters.
    """

    assert create_product(("123456789012345678901234567890"
                           "123456789012345678901234567890"
                           "12345678901234567890"),
                          valid_description, valid_price,
                          valid_email) is True
    assert create_product(("123456789012345678901234567890"
                           "123456789012345678901234567890"
                           "123456789012345678901"),
                          valid_description, valid_price,
                          valid_email) is False


def test_r4_3_product():
    """
    Testing R4-3: The description of the product can be arbitrary
      characters, with a minimum length of 20 characters and a
      maximum of 2000 characters.
    """

    assert create_product("Apple Pie 0", "",
                          valid_price, valid_email) is False
    assert create_product("Apple Pie 1", "1234567890",
                          valid_price, valid_email) is False
    assert create_product("Apple Pie 2", "12345678901234567890",
                          valid_price, valid_email) is True
    assert create_product("Apple Pie 3", "1234567890" * 200,
                          valid_price, valid_email) is True
    assert create_product("Apple Pie 4", "1234567890" * 200 + ".",
                          valid_price, valid_email) is False


def test_r4_4_product():
    """
    Testing R4-4: Description has to be longer than the product's
      title.
    """

    assert create_product("12345678901234567890",
                          "12345678901234567890",
                          valid_price, valid_email) is False
    assert create_product("1234567890123456789",
                          "12345678901234567890",
                          valid_price, valid_email) is True
    assert create_product("123456789012345678901",
                          "12345678901234567890",
                          valid_price, valid_email) is False


def test_r4_5_product():
    """
    Testing R4-4: Price has to be of range [10, 10000].
    """

    assert create_product("Apple Pie 5", valid_description, 900,
                          valid_email) is False
    assert create_product("Apple Pie 6", valid_description, 1000,
                          valid_email) is True
    assert create_product("Apple Pie 7", valid_description, 150000,
                          valid_email) is True
    assert create_product("Apple Pie 8", valid_description, 1000000,
                          valid_email) is True
    assert create_product("Apple Pie 9", valid_description, 1000001,
                          valid_email) is False


def test_r4_6_product():
    """
    Testing R4-6: last_modified_date must be after 2021-01-02 and
      before 2025-01-02.
    """

    # Testing R4-1 has already run, so the default product exists in
    # the database.
    product = get_product("Apple Pie", valid_email)
    assert product is not None
    assert product.last_modified_date > datetime.datetime(2021, 1, 2)
    assert product.last_modified_date < datetime.datetime(2025, 1, 2)


def test_r4_7_product():
    """
    Testing R4-7: owner_email cannot be empty. The owner of the
      corresponding product must exist in the database.
    """

    assert create_product("Apple Pie 11", valid_description,
                          valid_price, valid_email) is True
    product = get_product("Apple Pie 11", valid_email)
    assert product is not None
    assert product.owner_email is not None
    assert find_user(product.owner_email) is True


def test_r4_8_product():
    """
    Testing R4-8: A user cannot create products that have the same
      title.
    """

    assert create_product("Apple Pie 12", valid_description,
                          valid_price, valid_email) is True
    product = get_product("Apple Pie 12", valid_email)
    assert product is not None
    assert product.title == "Apple Pie 12"
    assert create_product("Apple Pie 12", valid_description,
                          valid_price, valid_email) is False


def test_r5_2_product():
    """
    Testing R5-2: Price can be only increased but cannot be decreased.
    """

    assert create_product("Test R52", valid_description,
                          1200, valid_email) is True
    assert update_product_price("Test R52", valid_email, 1300) is True
    assert update_product_price("Test R52", valid_email, 1100) is False


def test_r5_3_product():
    """
    Testing R5-3: last_modified_date should be updated when the update
    operation is successful.
    """

    assert create_product("Test R53", valid_description,
                          valid_price, valid_email) is True
    date = get_product("Test R53", valid_email).last_modified_date
    assert update_product_price("Test R53", valid_email, 2000) is True
    assert date < get_product("Test R53", valid_email).last_modified_date

    date = get_product("Test R53", valid_email).last_modified_date
    assert update_product_description("Test R53", valid_email,
                                      "abcdefghijklmnopqrstuvwxyz") is True
    assert date < get_product("Test R53", valid_email).last_modified_date

    date = get_product("Test R53", valid_email).last_modified_date
    assert update_product_title("Test R53", valid_email, "Test") is True
    assert date < get_product("Test", valid_email).last_modified_date

    date = get_product("Test", valid_email).last_modified_date
    assert update_product_quantity("Test", valid_email, 5) is True
    assert date < get_product("Test", valid_email).last_modified_date


def test_r5_4_product():
    """
    Testing R5-4: When updating an attribute, one has to make sure that it
    follows the same requirements as above.
    """

    assert create_product("Test R54", valid_description,
                          valid_price, valid_email) is True

    assert update_product_price("Test R54", valid_email, 900) is False
    assert update_product_price("Test R54", valid_email, 1100) is True

    assert update_product_description("Test R54", valid_email, "abc") is False
    assert update_product_description("Test R54", valid_email,
                                      "This is a very good product") is True

    assert update_product_title("Test R54", valid_email,
                                "This has a longer name than the description"
                                ) is False
    assert update_product_title("Test R54", valid_email, "R5") is True
    assert create_product("Name", valid_description,
                          valid_price, valid_email) is True
    assert update_product_title("R5", valid_email, "Name") is False
    assert update_product_title("R5", valid_email, " IDK") is False
    assert update_product_title("R5", valid_email, "IDK ") is False
    assert update_product_title("R5", valid_email, "I-D_K") is False

    assert update_product_quantity("R5", valid_email, -1) is False
    assert update_product_quantity("R5", valid_email, 0) is True
