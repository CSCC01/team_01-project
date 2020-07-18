from models import User
from exts import db
import hashlib


def insert_new_user(name, email, password1, password2, type):
    """
    Inserts user into User table.

    Args:
        name: The name given to the user. A string with max 64 characters.
        email: The email give to the user. A string with max 64 characters.
        password1: The hashed first password give by the user. A string with
          max 64 characters.
        password2: The hashed second password give by the user. A string with
          max 64 characters.
        type: The account access type. One of the following integer values:
          -1 == customer account.
           1 == owner account.
           0 == employee account.

    Returns:
        A touple containing any error messages raised and the user ID of the
        newly created user.
    """
    errmsg = []

    user = User.query.filter(User.email == email).first()
    if user:
        errmsg.append("Email has already been used.")
    if password1 != password2:
        errmsg.append("Passwords do not match.")
    if email == "":
        errmsg.append("An email is required.")
    if password1 == (hashlib.md5("".encode())).hexdigest():
        errmsg.append("A password is required.")

    # Adds user to db if no resistration errors occured
    if not errmsg:
        user = User(name=name, email=email, password=password1, type = type)
        db.session.add(user)
        db.session.commit()
        return None, user.uid

    return errmsg, None


def get_user_login(email, password):
    """
    Fetches a row from the User table.

    Retrieves a row pertaining the given email and password from the User table
    in the database.

    Args:
        email: The email pertaining to a user. A string.
        password: The hashed password pertaining to a user. A string.

    Returns:
        A user with matching email's and password's as the ones provided,
        None otherwise.
    """
    user = User.query.filter(User.email == email, User.password == password).first()
    return user
