###################################################
#                                                 #
#   Includes all routes to login and logout and   #
#   and logout.                                   #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
login_page = Blueprint('login_page', __name__, template_folder='templates')
from databaseHelpers.user import *

@login_page.route('/login', methods=['GET', 'POST'])
@login_page.route('/login.html', methods=['GET', 'POST'])
@login_page.route('/', methods = ['GET', 'POST'])
def login():
    # This runs when the user presses the login button
    if request.method == 'POST':
        # Grabs information from login feilds
        email =  request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()

        # Validates that the user exits in the database
        # If the user exists in the databse, they are logged in
        # If the user does not exist in the database, the user is redirected to the login page with an errmsg
        user = get_user_login(email, password)
        if user:
            session['account'] = user.uid
            session['type'] = user.type
            session.permanent = True
            return redirect(url_for('home_page.home'))
        else:
            return render_template("login.html", errmsg = "Failed to login: Incorrect email or password")

    # This runs if the user is already in seassion
    # If the user is already in session, it redirectes them to their homepage
    elif 'account' in session:
        return redirect(url_for('home_page.home'))

    # This runs if the user is not in seassion
    # Displays the login page
    else:
        return render_template("login.html")


# To end session you must logout
@login_page.route('/logout')
@login_page.route('/logout.html')
def logout():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    else:
        session.pop('account', None)
        session.pop('type', None)
        return redirect(url_for('login_page.login'))
