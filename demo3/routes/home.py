###################################################
#                                                 #
#   Includes all routes to home pages.            #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.user import *
from databaseHelpers.redeemedCoupons import *
from databaseHelpers.favourite import *

home_page = Blueprint('home_page', __name__, template_folder='templates')


# The home landing page
# Currently nothing is here
@home_page.route('/home')
@home_page.route('/home.html')
def home():
    # Redirects to login page if no user is signed it
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Customer view of home page
    elif session['type'] == -1:
        # Last 3 coupons purchased
        coupons = get_redeemed_coupons_by_uid(session["account"])[-3:]
        coupons.reverse()

        # Last 3 restaurants added to favourites
        restaurants = get_favourites(session['account'])[-3:]
        user = get_user(session['account'])
        return render_template('home.html', user = user, coupons = coupons, restaurants = restaurants)

    # owner / employee view of home page
    else:
        user = get_user(session['account'])
        return render_template('home.html', user = user)
