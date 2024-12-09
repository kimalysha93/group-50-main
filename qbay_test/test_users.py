"""
Testing file for users.py
"""

from qbay.users import login, register
from qbay.users import get_address, get_postal_code, get_balance, \
    update_user_name, update_shipping_address, update_postal_code

# Define any required variables for testing
valid_email = "test2@queensu.ca"
valid_password = "CiSc327!"


def test_r1_1_user():
    """
    R1-1: Both email and password cannot be empty
    """
    assert register("Park Jimin", "", "") is False
    assert register("Jotaro Kujo", "jojopt3@queensu.ca", "") is False
    assert register("Sasuke Uchiha", "", valid_password) is False
    assert register("Sesshoumaru", "mylord@queensu.ca",
                    valid_password) is True


def test_r1_2_user():
    """
    R1-2: A user is uniquely identified by their email address.
    """
    assert register("Makoto Niijima", "makochan@queensu.ca",
                    valid_password) is True
    assert register("Makoto Niijima", "imposter@queensu.ca",
                    valid_password) is True
    assert register("The Real Makoto", "makochan@queensu.ca",
                    valid_password) is False


def test_r1_3_user():
    """
    R1-3: The email has to follow addr-spec defined in RFC 5322
    """
    assert register("Tony Stark", "tonysus.ca",
                    valid_password) is False
    assert register("Peter Parker", "@spider@queensu.ca",
                    valid_password) is False
    assert register("Bruce Banner", "smash@queensu",
                    valid_password) is False
    assert register("Loki Best Boy", "sussybaka@queensu.ca",
                    valid_password) is True


def test_r1_4_user():
    """
    R1-4: Password has to meet the required complexity:
        minimum length 6,
        at least one upper case,
        at least one lower case,
        and at least one special character.
    """
    assert register("Apple", "bottomjeans@queensu.ca", "Gorb!") is False
    assert register("Boots", "withthefur@queensu.ca", "iluvgorb!") is False
    assert register("The Whole", "clubwaslookinather@queensu.ca",
                    "ILUVGORB!") is False
    assert register("She", "hitthefloor@queensu.ca", "ILuvGorb") is False
    assert register("Next", "thingyouknow@queensu.ca", "ILuvGorb!") is True


def test_r1_5_user():
    """
    R1-5: User name has to be non-empty,
        alphanumeric-only,
        and space allowed only if it is not as the prefix
        or suffix.
    """
    assert register("", "abreathtakingsight@queensu.ca",
                    valid_password) is False
    assert register("Imit@tions", "theymaybe@queensu.ca",
                    valid_password) is False
    assert register(" butTogether", "theymakeafine@queensu.ca",
                    valid_password) is False
    assert register("Spectacle ", "thoughthe@queensu.ca",
                    valid_password) is False
    assert register("Flowers of Evil", "blossom@queensu.ca",
                    valid_password) is True


def test_r1_6_user():
    """
    R1-6: User name has to be longer than 2 characters
        and less than 20 characters.
    """
    assert register("I", "wouldwalk@queensu.ca", valid_password) is False
    assert register("five hundred miles and I would walk five hundred more",
                    "justtobe@queensu.ca", valid_password) is False
    assert register("ThatMan", "whowalked1000miles@queensu.ca",
                    valid_password) is True


def test_r1_7_user():
    """
    R1-7: If the email has been used, the operation failed.
    """
    assert register('uwu0', 'test0@test.com', 'OwO123456!') is True
    assert register('uwu0', 'test1@test.com', 'OwO123456!') is True
    assert register('uwu1', 'test0@test.com', 'OwO123456!') is False


def test_r1_8_user():
    """
    R1-8: Shipping address is empty at the time of registration.
    """

    # Create a user for testing
    register("Goro Akechi", "deliciouspancakes@queensu.ca",
             "Und3sir4bleChi1d!")
    assert (get_address("deliciouspancakes@queensu.ca") == "") is True


def test_r1_9_user():
    """
    R1-9: Postal code is empty at the time of registration.
    """
    # Create a user for testing
    register("Karma Akabane", "assassinationclass@queensu.ca",
             "R3d.C0mb@t")
    assert (get_postal_code("assassinationclass@queensu.ca") == "") is True


def test_r1_10_user():
    """
    R1-10: Balance should be initialized as 100 at the time of registration.
        (free $100 dollar signup bonus).
    """
    # Create a user for testing
    register("Luck Voltia", "blackclover@queensu.ca", "#Z00M1n")
    assert (get_balance("blackclover@queensu.ca") == 10000) is True


def test_r2_1_login_success():
    """
    R2-1: A user can log in using her/his email address
        and the password.
    """

    # creating a user for testing
    register('Test User', valid_email, valid_password)

    assert login(valid_email, valid_password) is not None

    assert login(valid_email, "invalid_password") is None

    assert login("invalid_email", valid_password) is None

    assert login("invalid_email", "invalid_password") is None


def test_r2_2_login():
    """
    R2-2: The login function should check if the supplied inputs
        meet the same email/password requirements as above, before
        checking the database.
    """

    # correct email and password
    assert login(valid_email, valid_password) is not None

    # correct email but invalid password
    assert login(valid_email, "AbCdE|") is None

    # password isn't at least length 6
    assert login(valid_email, "") is None

    # password isn't at least length 6
    assert login(valid_email, "aBc1!") is None

    # password doesn't contain uppercase
    assert login(valid_email, "abcd1!") is None

    # password doesn't contain lowercase
    assert login(valid_email, "ABCD1!") is None

    # password doesn't contain special character
    assert login(valid_email, "abCDeFg") is None

    # password doesn't contain capital
    assert login(valid_email, "123456") is None

    # email follows addr-spec defined and correct password
    assert login("makochan@queensu.ca", valid_password) is not None

    # email doesn't follow addr-spec defined in RFC 5322
    assert login("!!!@queensu.ca", valid_password) is None

    # email doesn't follow addr-spec defined in RFC 5322
    assert login("", valid_password) is None


def test_r3_2_update_shipping_address():
    """
    R3-2: Shipping_address should be non-empty, alphanumeric-only,
    and no special characters such as !
    R3-1: A user is only able to update their user name,
    shipping_address, and postal_code, (restricted by this function)
    """

    # create more users
    register("TestBoy68", "sheeeeesh@yahoo.ca", "Sup3rCompl1d!")

    # valid new shipping address
    assert update_shipping_address("sheeeeesh@yahoo.ca",
                                   "123 Happy Street") is True

    # non empty
    assert update_shipping_address("sheeeeesh@yahoo.ca", "") is False

    # non alphanumeric (excluding spaces)
    assert update_shipping_address("sheeeeesh@yahoo.ca",
                                   "123 Happy Street!") is False


def test_r3_3_update_postal_code():
    """
    R3-3: Postal code has to be a valid Canadian postal code.
    R3-1: A user is only able to update their user name,
    shipping_address, and postal_code, (restricted by this function)
    """

    # create more users
    register("LightningMcqueen22", "kachow@yahoo.ca", "GamEr!")

    # valid new postal code
    assert update_postal_code("kachow@yahoo.ca", "K7L 7L7") is True

    # no space
    assert update_postal_code("kachow@yahoo.ca", "K7L7L7") is False

    # empty
    assert update_postal_code("kachow@yahoo.ca", "") is False

    # trailing space
    assert update_postal_code("kachow@yahoo.ca", "K7L7L7 ") is False

    # leading space
    assert update_postal_code("kachow@yahoo.ca", " K7L7L7") is False

    # special character
    assert update_postal_code("kachow@yahoo.ca", "K*L 7L7") is False


def test_r3_4_update_username():
    """
    R3-4: User name follows the requirements above.
    User name has to be non-empty, alphanumeric-only,
    and space allowed only if it is not as the prefix or suffix.
    User name has to be longer than 2 characters and less than 20 characters
    R3-1: A user is only able to update their user name,
    shipping_address, and postal_code, (restricted by this function)
    """

    # create more users
    register("Evan111", "spam@gmail.com", "Sup3rCompl1cated!")

    # valid new username
    assert update_user_name("spam@gmail.com", "TesterMan") is True

    # valid new username
    assert update_user_name("spam@gmail.com", "TesterMan22") is True

    # valid middle space
    assert update_user_name("spam@gmail.com", "Tester Man") is True

    # invalid prefix space
    assert update_user_name("spam@gmail.com", " TesterMan") is False

    # invalid suffix space
    assert update_user_name("spam@gmail.com", "TesterMan ") is False

    # alphanumeric only
    assert update_user_name("spam@gmail.com", "TesterMan!") is False
