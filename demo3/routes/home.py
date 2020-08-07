###################################################
#                                                 #
#   Includes all routes to home pages.            #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.user import *
from databaseHelpers.redeemedCoupons import *
from databaseHelpers.favourite import *

from databaseHelpers.achievementProgress import *
from databaseHelpers.employee import *
from databaseHelpers.restaurant import *


home_page = Blueprint('home_page', __name__, template_folder='templates')


# The home landing page
# Currently nothing is here
@home_page.route('/home')
@home_page.route('/home.html')
def home():
    # Redirects to login page if no user is signed it
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
      
    user = get_user(session['account'])
    # Customer view of home page
    if session['type'] == -1:
        # Last 3 coupons purchased
        coupons = get_redeemed_coupons_by_uid(session["account"])[-3:]
        coupons.reverse()

        # Last 3 restaurants added to favourites
        restaurants = get_favourites(session['account'])[-3:]
        return render_template('home.html', user = user, coupons = coupons, restaurants = restaurants)
     
        #Last 3 updated achievement progrss
        achievements_progress = get_recently_update_achievements(session['account'])
        achievements = get_updated_info(achievements_progress)

        return render_template('home.html', user = user, coupons = coupons,
                               restaurants = restaurants, achievements=achievements)

    # Employee view of home page
    elif session['type'] == 0:
        rid = get_employee_rid(session["account"])
        rname = get_restaurant_name_by_rid(rid)
        raddress = get_restaurant_address(rid)
        return render_template('home.html', rname = rname, raddress = raddress, user = user)

    # default view of home page
    else:
        return render_template('home.html', user = user)
