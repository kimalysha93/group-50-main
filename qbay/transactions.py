"""
File contains functionality relating to transactions and
product ordering
"""

import datetime
from qbay.models import Transaction
from qbay.users import decrease_balance, get_user, get_userid, increase_balance
from qbay.products import get_product, get_productid, update_product_quantity
from qbay import db


def order_product(title, requested_quantity, buyer_email, owner_email):
    """
    Order a product
      Parameters:
        title (string):             product title
        requested_quantity (int):   product price
        buyer_email (string):       email of buyer
        owner_email (string) :      product owner email
      Returns:
        True if the product was successfully ordered, otherwise False
    """

    product = get_product(title, owner_email)
    buyer = get_user(buyer_email)
    total_price = product.price * requested_quantity

    # Requirement: A user cannot place an order for their own products.
    if (buyer_email == owner_email):
        return False

    # Requirement: A user cannot place an order that costs
    # more than their balance.
    if (not check_balance(total_price, buyer.balance)):
        return False

    # User shouldn't be able to request more than the number of instances
    # of the product that currently exists
    if (not check_quantity(product.quantity, requested_quantity)):
        return False

    # If requirements are passed, the order is placed and balances are updated.
    update_user_balances(buyer_email, owner_email, total_price)

    # quantity is updated
    new_quantity = product.quantity - requested_quantity
    update_product_quantity(title, owner_email, new_quantity)

    current_date = datetime.datetime.now()
    db.session.add(Transaction(buyer=get_userid(buyer_email),
                               seller=get_userid(owner_email),
                               product_id=get_productid(title, owner_email),
                               total_price=total_price,
                               date=current_date,
                               quantity=requested_quantity,
                               purchased=True,
                               delivered=True))
    return True


def check_balance(total_price, balance):
    """
    Checks that the buyer can afford the cost of the order
      Parameters:
        total_price (int):      total price of order
        balance (int):          current balance of the buyer
      Returns:
        True if the User's balance is greater than or equal to the
        total price of the order, otherwise False
    """
    return (balance >= total_price)


def check_quantity(current_quantity, requested_quantity):
    """
    Checks if the Product's current quantity is greater than or equal
    to the requested quantity in the order
      Parameters:
        current_quantity (int):      current quantity of the product
        requested_quantity (int):    quantity requested by the buyer
      Returns:
        True if the Product's current quantity is greater than or equal
        to the requested quantity in the order, otherwise False
    """
    return (current_quantity - requested_quantity >= 0)


def update_user_balances(buyer_email, owner_email, total_price):
    """
    Updates the balances of the Buyer and Seller after a successful transaction
      Parameters:
        buyer_email (string):       buyer email
        owner_email (string):       product owner email
        total_price (int):          total cost of the transaction
    """
    decrease_balance(buyer_email, total_price)
    increase_balance(owner_email, total_price)
