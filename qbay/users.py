"""
File contains functions for user login, register and many
    other user specific functions
"""

import re
from qbay.models import User
from qbay import db


def valid_login(email, password):
    """
    Checks login information meets requirements
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        Bool True if the email and password are valid,
        False otherwise
    """

    # R2-2: check if the supplied inputs meet the email/password requirements
    # validates password
    req_email = re.compile(
        "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)")
    if ((len(password) >= 6) and
            re.search('[@_!#$%^&*()<>?||}{~:]', password) and
            re.search("[a-z]", password) and
            re.search("[A-Z]", password)):
        # The email has to follow addr-spec defined in RFC 5322
        if not(re.search(req_email, email)):
            return False
        return True
    return False


def login(email, password):
    """
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    """

    # R2-1: User can log in using email address and the password
    # R2-2: check supplied inputs meet requirements before checking database
    if (valid_login(email, password)):
        valid = db.session.query(User).filter_by(email=email,
                                                 password=password).first()
        if valid is None:
            return None
        return valid
    return None


def find_user(email):
    """
    Checks if a given email belongs to a user
    Parameters:
        email (string): user email
      Returns:
        True if the email is being used in the database, False otherwise
    """
    if (db.session.query(User).filter_by(email=email).first() is None):
        return False
    return True


def get_user(email):
    """
    Returns an existing product
      Parameters:
        title (string):         product title
        owner_email (string) : product owner email
      Returns:
        A Product object if the product exists in the database,
        otherwise None
    """
    return db.session.query(User).filter_by(email=email).first()


def get_userid(email):
    """
    Returns the id of a given user
    Parameters:
        email (string): user email
      Returns:
        The id of the user
    """
    return db.session.query(User).filter_by(
        email=email).first().id


def get_address(email):
    """
    Returns the address object of a given user
    Parameters:
        email (string): user email
      Returns:
        The shipping address of the user
    """
    # R1-8: Shipping address is empty at the time of registration.
    return db.session.query(User).filter_by(
        email=email).first().shipping_address


def get_postal_code(email):
    """
    Returns the address object of a given user
    Parameters:
        email (string): user email
      Returns:
        The postal code of the user
    """
    # R1-9: Postal code is empty at the time of registration.
    return db.session.query(User).filter_by(email=email).first().postal_code


def get_balance(email):
    """
    Returns the address object of a given user
    Parameters:
        email (string): user email
      Returns:
        The current balance of the user
    """
    # R1-10: Balance should be initialized as 100 at the time of registration.
    # (free $100 dollar signup bonus).
    return db.session.query(User).filter_by(email=email).first().balance


def register(user_name, email, password):
    """
    Register a new user
      Parameters:
        user_name (string):     user name
        email (string):         user email
        password (string):      user password
      Returns:
        True if registration succeeded otherwise False
    """

    # R1-1: Both email and password cannot be empty
    if len(email) == 0 or len(password) == 0:
        return False

    # R1-2: A user is uniquely identified by their email address.
    if (not(db.session.query(User).filter_by(email=email).first() is None)):
        return False

    # R1-3: The email has to follow addr-spec defined in RFC 5322
    req_email = re.compile(
        "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)")
    if not(re.search(req_email, email)):
        return False

    # R1-4: Password has to meet the required complexity:
    #    minimum length 6,
    #    at least one upper case,
    #    at least one lower case,
    #    and at least one special character.
    if not ((len(password) >= 6) and
            re.search('[@_!#$%^&*()<>?||}{~:]', password) and
            re.search("[a-z]", password) and
            re.search("[A-Z]", password)):
        return False

    # R1-5: User name has to be non-empty,
    #    alphanumeric-only,
    #    and space allowed only if it is not as the prefix
    #    or suffix.

    req_name = re.compile(
        "^[a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9]{1,}$")
    if not re.search(req_name, user_name):
        return False

    # R1-6: User name has to be longer than 2 characters
    #    and less than 20 characters.

    if len(user_name) < 2 or len(user_name) >= 20:
        return False

    # R1-7: If the email has been used, the operation failed.
    if (not(db.session.query(User).filter_by(email=email).first() is None)):
        return False

    # create a new user
    user = User(email=email,
                user_name=user_name,
                password=password,
                shipping_address="",
                postal_code="",
                balance=10000,
                order_history=[])

    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def update_shipping_address(email, new_shipping_address):
    """
    Register a new user
      Parameters:
        email (string):                 user email
        new_shipping_address (string):  new shipping address
      Returns:
        True if new_shipping_address was sucessfully updated,
        otherwise False
    """

    """
    R3-2: Shipping_address should be non-empty,
    alphanumeric-only, and no special characters.
    """
    # not empty
    if len(new_shipping_address) > 0:
        for x in range(0, len(new_shipping_address)):
            # alpha numeric-only
            if (not new_shipping_address[x].isalnum()):
                # spaces are allowed
                if (new_shipping_address[x] != " "):
                    return False
        person_update = db.session.query(User).filter_by(email=email).first()
        if person_update is not None:
            person_update.shipping_address = new_shipping_address
            db.session.commit()
            return True
        else:
            return False
    else:
        return False


def update_postal_code(email, new_postal_code):
    """
    Register a new user
      Parameters:
        email (string):             user email
        new_postal_code (string):   new postal code
      Returns:
        True if new_postal_code was sucessfully updated,
        otherwise False
    """

    # R3-3: Postal code has to be a valid Canadian postal code.
    # not empty
    if len(new_postal_code) == 7:
        for x in range(0, len(new_postal_code)):
            # alternate number and letter, one space in the middle
            if (x == 0 or x == 2 or x == 5):
                if (not new_postal_code[x].isalpha()):
                    return False
            elif (x == 3 and new_postal_code[x] != " "):
                return False
            elif (x == 1 or x == 4 or x == 6):
                if (not new_postal_code[x].isdecimal()):
                    return False
        person_update = db.session.query(User).filter_by(email=email).first()
        if person_update is not None:
            person_update.postal_code = new_postal_code
            db.session.commit()
            return True
        else:
            return False
    else:
        return False


def update_user_name(email, new_user_name):
    """
    Register a new user
      Parameters:
        email (string):         user email
        new_user_name (string):  new username
      Returns:
        True if new_user_name was sucessfully updated,
        otherwise False
    """

    # R3-4: User name follows the requirements above.
    # username greater than 2 and less than 20
    if (len(new_user_name) > 2 and len(new_user_name) < 20):
        for x in range(0, len(new_user_name)):
            if (not new_user_name[x].isalnum()):
                # prefix or suffix spaces are not allowed
                if (new_user_name[x] == " " and
                        (x == 0 or x == (len(new_user_name) - 1))):
                    return False
                # no special characters allowed
                elif (new_user_name[x] != " "):
                    return False
        person_update = db.session.query(User).filter_by(email=email).first()
        if person_update is not None:
            person_update.user_name = new_user_name
            db.session.commit()
            return True
        else:
            return False
    else:
        return False


def decrease_balance(email, balance_loss):
    get_user(email).balance = get_user(email).balance - balance_loss


def increase_balance(email, balance_gain):
    get_user(email).balance = get_user(email).balance + balance_gain
