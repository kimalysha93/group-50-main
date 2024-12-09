from os import name
from flask import render_template, request, session, redirect

from qbay.models import Product, Transaction, User
from qbay.products import (create_product, update_product_description,
                           update_product_price, update_product_quantity,
                           update_product_title)
from qbay.users import login, register, update_user_name, \
    update_shipping_address, update_postal_code, get_userid
from qbay.transactions import order_product
from qbay import app, db
from functools import wraps


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """
    @wraps(inner_function)
    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = db.session.query(User).filter_by(
                    email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    """
    login get request
    return: login render template
    """

    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    """
    login post request
    """

    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information
        between a user's browser and the end server.
        Typically it is packed and stored in the browser cookies.
        They will be past along between every request the browser made
        to this services. Here we store the user object into the
        session, so we can tell if the client has already login
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/', methods=["GET"])
@authenticate
def home(user):
    """
    Get request for the home page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The main HTML page (if the user is logged in).
    """
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # Current product data
    products = db.session.query(Product).filter_by(
        owner_email=user.email).all()

    return render_template('index.html', user=user, products=products)


@app.route('/', methods=["POST"])
@authenticate
def home_post(user):
    """
    Post request for the home page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The update product HTML (if logged in).
    """
    print("Index page post request recieved.")
    product_title = request.form.get("product_title")
    session["product_title"] = product_title

    return redirect('/update-product')


@app.route('/register', methods=['GET'])
def register_get():
    """
    register get request
    return: register render template
    """

    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    """
    register post request
    """

    email = request.form.get('email')
    user_name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(user_name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/update-profile', methods=['GET'])
@authenticate
def update_profile_get(user):
    """
    Get request for the update profile page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The update profile HTML page (if the user is logged in).
    """
    return render_template('update-profile.html', user=user,
                           message='')


@app.route('/update-profile', methods=['POST'])
@authenticate
def update_profile_post(user):
    """
    Post request for the update profile page. Updates profile information
    in the database if they meet the requirements.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The main HTML page if profile update is successful, otherwise returns
        the update profile page HTML page (if the user is logged in).
    """
    user_name = request.form.get('name')
    shipping_address = request.form.get('shipping_address')
    postal_code = request.form.get('postal_code')
    error_message = None

    # each update gets their own button for now
    if request.form["submit-button"] == "Update Username":
        success = update_user_name(user.email, user_name)
        if not success:
            error_message = "Failed to Update Username"
    elif request.form["submit-button"] == "Update Shipping Address":
        success = update_shipping_address(user.email, shipping_address)
        if not success:
            error_message = "Failed to Update Shipping Address"
    elif request.form["submit-button"] == "Update Postal Code":
        success = update_postal_code(user.email, postal_code)
        if not success:
            error_message = "Failed to Update Postal Code"

    if error_message:
        return render_template('update-profile.html', user=user,
                               message=error_message)
    else:
        return redirect('/')


@app.route('/product-creation', methods=['GET'])
@authenticate
def product_creation_get(user):
    """
    Get request for the product creation page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The product creation HTML page (if the user is logged in).
    """
    return render_template('product-creation.html', user=user,
                           message='Create a product')


@app.route('/product-creation', methods=['POST'])
@authenticate
def product_creation_post(user):
    """
    Post request for the product creation page. Adds a product to the database
    if the product meets the requirements.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The main HTML page if product creation is successful, otherwise returns
        the product creation HTML page (if the user is logged in).
    """
    print("Attempting POST method.")
    title = request.form.get('product-name')
    description = request.form.get('description')
    price = int(request.form.get('price')) * 100  # convert to cents
    quantity = int(request.form.get('quantity'))
    error_message = None

    # use backend api to create the product
    success = create_product(title, description, price, session['logged_in'],
                             quantity)
    if not success:
        error_message = "Product creation failed."

    # if there is any error when creating the product,
    # then stay on the product creation page (otherwise go to
    # the home page)
    if error_message:
        return render_template('product-creation.html', user=user,
                               message=error_message)
    else:
        return redirect('/')


@app.route('/update-product', methods=['GET'])
@authenticate
def update_product_get(user):
    """
    Get request for the update product page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The update product HTML page (if the user is logged in).
    """
    print("Attempting to GET update-product page.")
    product = db.session.query(Product).filter_by(owner_email=user.email,
                                                  title=session
                                                  ["product_title"]).first()
    print("Found product, return HTML page. Product title: ", product.title)

    return render_template('update-product.html', user=user, product=product)


@app.route('/update-product', methods=['POST'])
@authenticate
def update_product_post(user):
    """
    Post request for the update product page. Modifies a product's
    information to the database if the change still satisfies the
    requirements.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The main HTML page if the product update is successful, otherwise
        returns the update product HTML page (if the user is logged
        in).
    """
    print("Attempting POST method.")
    new_title = request.form.get('product-name')
    new_description = request.form.get('description')
    new_price = request.form.get('price')
    new_quantity = request.form.get('quantity')
    error_message = None

    product = db.session.query(Product).filter_by(owner_email=user.email,
                                                  title=session
                                                  ["product_title"]).first()

    success = True
    if (not(new_title == "")):
        success = success and update_product_title(product.title,
                                                   session['logged_in'],
                                                   new_title)

    if (not(new_description == "")):
        success = success and update_product_description(product.title,
                                                         session['logged_in'],
                                                         new_description)

    if (not(new_price == "")):
        success = success and update_product_price(product.title,
                                                   session['logged_in'],
                                                   int(new_price) * 100)

    if (not(new_quantity == "")):
        success = success and update_product_quantity(product.title,
                                                      session['logged_in'],
                                                      int(new_quantity))

    if not success:
        error_message = "Update failed."

    # if there is any error when creating the product,
    # then stay on the product creation page (otherwise go to
    # the home page)
    if error_message:
        return render_template('update-product.html',
                               product=product,
                               user=user,
                               message=error_message)
    else:
        return redirect('/')


@app.route('/shop', methods=['GET'])
@authenticate
def shop_get(user):
    """
    Get request for the shop page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The shop HTML page (if the user is logged in).
    """
    # Only display products that the current user is not selling
    products = [p for p in db.session.query(Product).all()
                if (p.owner_email != user.email) and (p.quantity > 0)]
    return render_template('shop.html', user=user, products=products,
                           message="")


@app.route('/shop', methods=["POST"])
@authenticate
def shop_post(user):
    """
    Post request for the shop page.
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The shop HTML (if the user is logged in).
    """
    product_title = request.form.get("product_title")
    session["product_title"] = product_title

    return redirect('/checkout')


@app.route('/checkout', methods=['GET'])
@authenticate
def checkout_get(user):
    """
    Get request for the checkout page
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The checkout HTML page (if the user is logged in).
    """
    product = db.session.query(Product).filter_by(title=session
                                                  ["product_title"]).first()

    return render_template('checkout.html', user=user, product=product,
                           message="Checkout")


@app.route('/checkout', methods=['POST'])
@authenticate
def checkout_post(user):
    """
    Post request for the checkout page
      Parameters:
        user (User) : a User object representing the user currently logged in
      Returns:
        The shop HTML page (if the user is logged in).
    """
    product = db.session.query(Product).filter_by(title=session
                                                  ["product_title"]).first()

    error_message = None
    new_quantity = request.form.get('quantity')
    success = False
    if new_quantity != "":
        success = order_product(product.title, int(new_quantity), user.email,
                                product.owner_email)
    if not success:
        error_message = "Unable to purchase product."

    if error_message:
        return render_template('checkout.html',
                               product=product,
                               user=user,
                               error=error_message)
    else:
        return redirect('/shop')
