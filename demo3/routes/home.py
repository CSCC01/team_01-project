###################################################
#                                                 #
#   Includes all routes to home pages.            #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint

from databaseHelpers.redeemedCoupons import *
from databaseHelpers.achievement import *
from databaseHelpers.achievementProgress import *
from databaseHelpers.restaurant import *
from databaseHelpers.employee import *
from databaseHelpers.user import *
from datetime import datetime
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

    user = get_user(session['account'])
    # Customer view of home page
    if session['type'] == -1:
        # Last 3 coupons purchased
        coupons = get_redeemed_coupons_by_uid(session["account"])[-3:]
        coupons.reverse()

        # Last 3 restaurants added to favourites
        restaurants = get_favourites(session['account'])[-3:]
        return render_template('home.html', user = user, coupons = coupons, restaurants = restaurants)

    # Employee view of home page
    elif session['type'] == 0:
        rid = get_employee_rid(session["account"])
        rname = get_restaurant_name_by_rid(rid)
        raddress = get_restaurant_address(rid)
        return render_template('home.html', rname = rname, raddress = raddress, user = user)

    # Owner view of home page
    elif session['type'] == 1:
        rid = get_rid(session["account"])
        rname = get_restaurant_name_by_rid(rid)
        raddress = get_restaurant_address(rid)
        coupons = get_redeemed_coupons_by_rid(rid)

        # get 3 top owned coupons
        top_owned_coupons = coupons.copy()
        top_owned_coupons.sort(key=lambda x: x.get('holders'))
        top_owned_coupons = top_owned_coupons[-3:]
        top_owned_coupons.reverse()
        
        # get 3 top used coupons
        top_used_coupons = coupons.copy()
        top_used_coupons.sort(key=lambda x: x.get('used'))
        top_used_coupons = top_used_coupons[-3:]
        top_used_coupons.reverse()

        # get the 3 achievements started by the most customers
        achievements = get_achievements_with_progress_entry_count(get_achievements_by_rid(rid))
        achievements.sort(key=lambda x: x.get('progress_entries'))
        achievements = achievements[-3:]
        achievements.reverse()

        return render_template('home.html', rname = rname, raddress = raddress, today = date.today(),
                                top_owned_coupons = top_owned_coupons, top_used_coupons = top_used_coupons,
                                achievements = achievements, user = user)

    # default view of home page
    else:
        return render_template('home.html', user = user)
