###################################################
#                                                 #
#   Includes all routes to profile pages.         #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
profile_page = Blueprint('profile_page', __name__, template_folder='templates')

from databaseHelpers.restaurant import *

@profile_page.route('/profile.html')
@profile_page.route('/profile')
def profile():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    else:

        # if user is a restaurant owner
        if session['account'] == 1:
            rid = get_rid(session['account'])
            rname = get_restaurant_name_by_rid(rid)
            raddress = get_restaurant_address(rid)

            return render_template('profile.html', rname = rname, raddress = raddress)

        return render_template('profile.html')

@profile_page.route('/editRestaurantInfo.html', methods=['GET', 'POST'])
@profile_page.route('/editRestaurantInfo', methods=['GET', 'POST'])
def edit_restaurant_info():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    
    # if user is a restaurant owner
    if session['type'] == 1:
        rid = get_rid(session['account'])
        rname = get_restaurant_name_by_rid(rid)
        raddress = get_restaurant_address(rid)

        if request.method == 'POST':
            rname = request.form['rname']
            raddress = request.form['address']
            restaurant = get_resturant_by_rid(rid)

            errmsg = update_restaurant_information(restaurant, rname, raddress)
            
            if not errmsg:
                return redirect(url_for('profile_page.profile'))
            return render_template('editRestaurantInfo.html', rname = rname, raddress = raddress, errmsg = errmsg)

        return render_template('editRestaurantInfo.html', rname = rname, raddress = raddress)
    else:
        return redirect(url_for('home_page.home'))

