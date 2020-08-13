###################################################
#                                                 #
#   Includes all routes to registration pages.    #
#   This currently includes customer, employee,   #
#   and owner registration.                       #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.user import *
from databaseHelpers.restaurant import *
from databaseHelpers.employee import *

registration_page = Blueprint('registration_page', __name__, template_folder='templates')

# The registration options page
@registration_page.route('/registration.html')
@registration_page.route('/registration')
def registration():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home_page.home'))
    else:
        return render_template('registration.html')


# Customer register
@registration_page.route('/registration0', methods=['GET', 'POST'])
@registration_page.route('/registration0.html', methods=['GET', 'POST'])
def user_register():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home_page.home'))

    # A list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()

        errmsg, uid = insert_new_user(name, email, password, password2, -1)
        if not errmsg:
            return redirect(url_for('login_page.login'))
    return render_template("registration0.html", errmsg=errmsg)


# Owner register
@registration_page.route('/registration1', methods=['GET', 'POST'])
@registration_page.route('/registration1.html', methods=['GET', 'POST'])
def owner_register():
    # If someone is already logged in they get redirected to the home page
    if 'account' in session:
        return redirect(url_for('home_page.home'))

    # A list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()
        address = request.form['address']
        rname = request.form['rname']

        errmsg, uid = insert_new_user(name, email, password, password2, 1)
        errmsg = get_errmsg_registration(rname, address, errmsg)

        if uid:
            insert_new_restaurant(rname, address, uid)
            return redirect(url_for('login_page.login'))

    return render_template("registration1.html", errmsg=errmsg)



# Employee registration
@registration_page.route('/registration2', methods=['GET', 'POST'])
@registration_page.route('/registration2.html', methods=['GET', 'POST'])
def employee_register():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    if session['type'] != 1:
        return redirect(url_for('home_page.home'))

    # An list of all the errors that will be displayed to the user if login fails
    errmsg = []
    if request.method == 'POST':
        # Grabs information from signup fields
        name = request.form['name']
        email = request.form['email']
        password = (hashlib.md5(request.form['password'].encode())).hexdigest()
        password2 = (hashlib.md5(request.form['password2'].encode())).hexdigest()

        errmsg, uid = insert_new_user(name, email, password, password2, 0)

        if uid:
            rid = get_rid(session["account"])
            insert_new_employee(uid, rid)
            return redirect(url_for('employee_page.employee'))

    return render_template("registration2.html", errmsg=errmsg)


@registration_page.route('/login', methods=['GET', 'POST'])
@registration_page.route('/login.html', methods=['GET', 'POST'])
@registration_page.route('/', methods = ['GET', 'POST'])
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
