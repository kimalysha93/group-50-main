from qbay import db


class User(db.Model):
    """Represents the main User base class

    Keyword arguments:
    db.Model -- the database storing all relevant transaction information
    """
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    shipping_address = db.Column(db.String(120), unique=False, nullable=False)
    postal_code = db.Column(db.String(6), unique=False, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    order_history = []  # this will be populated by a DB search of transactions

    def __repr__(self):
        return '<User %r>' % self.user_name


class Buyer(User):
    """Represent the Buyer
    """
    cart = []  # this will be populated later by a function


class Seller(User):
    """ Represent the Seller
    """
    products = []


class Product(db.Model):
    """Represents the Product class
    Keyword arguments:
    db.Model -- the database storing all relevant Product information
    """
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    last_modified_date = db.Column(db.DateTime, nullable=False)
    owner_email = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reviews = []  # list of review object ids

    def __repr__(self):
        return '<ID %r>' % self.id


class Transaction(db.Model):
    """Represent a transaction between a seller and buyer of a specific item.

    Keyword arguments:
    db.Model -- the database storing all relevant transaction information
    """
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    buyer = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchased = db.Column(db.Boolean, nullable=False)
    delivered = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<ID %r>' % self.id


class Review(db.Model):
    """Represent a review from a buyer for a specific item.

    Keyword arguments:
    db.Model -- the database storing all relevant transaction information
    """
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    buyer = db.Column(db.Integer, nullable=False)   # user_email
    score = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return '<ID %r>' % self.id


# create all tables
db.create_all()
