###################################################
#                                                 #
#   Includes all routes to home pages.            #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.restaurant import *
from databaseHelpers.employee import *
from databaseHelpers.user import *

home_page = Blueprint('home_page', __name__, template_folder='templates')


# The home landing page
# Currently nothing is here
@home_page.route('/home')
@home_page.route('/home.html')
def home():
    # Redirects to login page if no user is signed it
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Employee view of home page
    elif session['type'] == 0:
        rid = get_employee_rid(session["account"])
        rname = get_restaurant_name_by_rid(rid)
        raddress = get_restaurant_address(rid)
        return render_template('home.html', rname = rname, raddress = raddress)

    # owner / employee view of home page
    else:
        return render_template('home.html')
