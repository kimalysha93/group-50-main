"""
File contains functionality relating to product creation and
modification.
"""

import datetime
import re
from qbay.models import Product
from qbay.users import find_user
from qbay import db


def create_product(title, description, price, owner_email, quantity=1):
    """
    Creates a new product
      Parameters:
        title (string):        product title
        description (string):  product description
        price (int):           product price
        owner_email (string) : product owner email
      Returns:
        True if the product was successfully created, otherwise False
    """

    # Validate title and description (R4-1, R4-2, R4-3, R4-4, R4-8 check)
    if (not(valid_title(title, description) and
            valid_description(title, description))):
        return False

    # Validate price (R4-5)
    if (not(valid_price(price))):
        return False

    # R4-6: last_modified_date must be after 2021-01-02 and before
    # 2025-01-02.
    last_modified_date = datetime.datetime.now()
    if (not(valid_date(last_modified_date))):
        return False

    # R4-7: owner_email cannot be empty. The owner of the
    # corresponding product must exist in the database.
    if (owner_email is None or owner_email == "" or
            not(find_user(owner_email))):
        return False

    # Add product to the database
    db.session.add(Product(title=title, description=description,
                           price=price,
                           last_modified_date=last_modified_date,
                           owner_email=owner_email,
                           quantity=quantity, reviews=[]))

    db.session.commit()

    return True


def get_product(title, owner_email):
    """
    Returns an existing product
      Parameters:
        title (string):         product title
        owner_email (string) : product owner email
      Returns:
        A Product object if the product exists in the database,
        otherwise None
    """
    return db.session.query(Product).filter_by(title=title,
                                               owner_email=owner_email).first()


def get_productid(title, owner_email):
    """
    Returns the id of a given product
    Parameters:
        email (string): user email
      Returns:
        The id of the product
    """
    return db.session.query(Product).filter_by(
        title=title,
        owner_email=owner_email).first().id


def update_product_description(title, owner_email, description):
    """
    Updates a given product's description
      Parameters:
        title (string):       product title
        owner_email (string): product owner email
        description (string): new product description
    """
    # Get access to the product
    product = get_product(title, owner_email)
    if (product is None):
        return False

    # Validate description (R4-3, R4-4 check)
    if (not(valid_description(title, description))):
        return False

    product.description = description

    # R4-6: last_modified_date must be after 2021-01-02 and before
    # 2025-01-02
    #
    # R5-3: last_modified_date should be updated when the update operation is
    # successful.
    last_modified_date = datetime.datetime.now()
    if (not(valid_date(last_modified_date))):
        return False
    product.last_modified_date = last_modified_date

    db.session.commit()
    return True


def update_product_price(title, owner_email, price):
    """
    Updates a given product's price
      Parameters:
        title (string):       product title
        owner_email (string): product owner email
        price (int):          new product price
    """
    # Get access to the product
    product = get_product(title, owner_email)
    if (product is None):
        return False

    # R4-5: Price has to be of range [10, 10000].
    # R5-2: Price can be only increased but cannot be decreased.
    if (not(valid_price(price)) or price <= product.price):
        return False

    product.price = price

    # R4-6: last_modified_date must be after 2021-01-02 and before
    # 2025-01-02
    #
    # R5-3: last_modified_date should be updated when the update operation is
    # successful.
    last_modified_date = datetime.datetime.now()
    if (not(valid_date(last_modified_date))):
        return False
    product.last_modified_date = last_modified_date

    db.session.commit()
    return True


def update_product_title(title, owner_email, new_title):
    """
    Updates a given product's title
      Parameters:
        title (string):       product title
        owner_email (string): product owner email
        new_title (string):   new product title
    """
    # Get access to the product
    product = get_product(title, owner_email)
    if (product is None):
        return False

    # Validate title (R4-1, R4-2, R4-4, R4-8 check)
    if (not(valid_title(new_title, product.description))):
        return False

    product.title = new_title

    # R4-6: last_modified_date must be after 2021-01-02 and before
    # 2025-01-02
    # R5-3: last_modified_date should be updated when the update operation is
    # successful.
    last_modified_date = datetime.datetime.now()
    if (not(valid_date(last_modified_date))):
        return False
    product.last_modified_date = last_modified_date

    db.session.commit()
    return True


def update_product_quantity(title, owner_email, quantity):
    """
    Updates a given product's quantity
      Parameters:
        title (string):       product title
        owner_email (string): product owner email
        quantity (int):       new product quantity
    """
    # Get access to the product
    product = get_product(title, owner_email)
    if (product is None):
        return False

    # Check for valid quantities.
    if (quantity < 0):
        return False

    product.quantity = quantity

    # R4-6: last_modified_date must be after 2021-01-02 and before
    # 2025-01-02
    #
    # R5-3: last_modified_date should be updated when the update operation is
    # successful.
    last_modified_date = datetime.datetime.now()
    if (not(valid_date(last_modified_date))):
        return False
    product.last_modified_date = last_modified_date

    db.session.commit()
    return True


def valid_title(title, description):
    """
    Checks that the given title is valid
    (meets R4-1, R4-2, R4-4, R4-8).
      Parameters:
        title (string):       product title
        description (string): product description
      Returns:
        True if the product title is valid, otherwise False
    """
    # R4-1: The title of the product has to be alphanumeric-only, and
    # space allowed only if it is not as prefix and suffix.
    # ^[a-zA-Z0-9]$| = any single alphanumeric OR
    # ^[a-zA-Z0-9] = begins with an alphanumeric
    # [a-zA-Z0-9\s]* = some number (or 0) alphanumerics or spaces
    # [a-zA-Z0-9]$ = ends with an alphanumeric
    if (not(bool(re.match("^[a-zA-Z0-9]$|"
                          "^[a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9]$",
                          title)))):
        return False

    # R4-2: The title of the product is no longer than 80 characters.
    if (len(title) > 80):
        return False

    # R4-4: Description has to be longer than the product's title.
    if (len(description) <= len(title)):
        return False

    # R4-8: A user cannot create products that have the same title.
    if (not(db.session.query(Product).filter_by(title=title).first() is None)):
        return False

    return True


def valid_description(title, description):
    """
    Checks that the given description is valid
    (meets R4-3 R4-4).
      Parameters:
        title (string):       product title
        description (string): product description
      Returns:
        True if the product description is valid, otherwise False
    """
    # R4-3: The description of the product can be arbitrary
    # characters, with a minimum length of 20 characters and a
    # maximum of 2000 characters.
    if (len(description) < 20 or len(description) > 2000):
        return False

    # R4-4: Description has to be longer than the product's title.
    if (len(description) <= len(title)):
        return False

    return True


def valid_price(price):
    """
    Checks that the given price is valid
    (meets R4-5).
      Parameter:
        price (int): product price
      Returns:
        True if the product price is valid, otherwise False
    """
    # R4-5: Price has to be of range [10, 10000].
    if (price < 1000 or price > 1000000):
        return False

    return True


def valid_date(date):
    """
    Checks that the current date and time are valid
    (meets R4-6).
      Parameter:
        date (datetime): a datetime object
      Returns:
        True if the date and time are valid, otherwise False
    """
    early_bound = datetime.datetime(2021, 1, 2)
    late_bound = datetime.datetime(2025, 1, 2)

    # R4-6: last_modified_date must be after 2021-01-02 and before
    # 2025-01-02.
    if (early_bound > date or late_bound < date):
        return False

    return True
