###################################################
#                                                 #
#   Includes all routes to the search pages.      #
#   This includes search, restaurant home, and    #
#   coupon offers.                                #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.restaurant import *
from databaseHelpers.coupon import *
from databaseHelpers.achievement import *
from databaseHelpers.achievementProgress import *
from databaseHelpers.redeemedCoupons import *
from databaseHelpers.points import *
from databaseHelpers.experience import *
from databaseHelpers.level import *
search_page = Blueprint('search_page', __name__, template_folder='templates')


@search_page.route('/search.html', methods=['GET', 'POST'])
@search_page.route('/search', methods=['GET', 'POST'])
def search():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home_page.home'))

    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form['query']
            restaurants = get_resturant_by_name(query)
            return render_template('search.html', restaurants = restaurants, query = request.form['query'])
        if 'rid' in request.form:
            rid = request.form['rid']
            return redirect(url_for('search_page.restaurant', rid=rid))
    else:
        return render_template('search.html')


@search_page.route('/restaurant<rid>.html', methods=['GET', 'POST'])
@search_page.route('/restaurant<rid>', methods=['GET', 'POST'])
def restaurant(rid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home_page.home'))

    restaurant = get_resturant_by_rid(rid)
    if restaurant:
        # Gets coupons
        rname = get_restaurant_name_by_rid(rid)
        coupons = filter_valid_coupons(get_coupons(rid))[-3:]
        coupons.reverse()

        # Gets achievements
        achievements = get_recently_started_achievements(get_achievements_by_rid(rid), session['account'])

        # Gets point progress
        uid = session['account']
        if not get_points(uid, rid):
            insert_points(uid, rid)
        if not get_experience(uid, rid):
            insert_experience(uid, rid)
        experience = get_experience(uid, rid).experience
        level = convert_experience_to_level(experience)
        return render_template("restaurant.html", restaurant = restaurant, level = level,
                                overflow = get_experience_since_last_level(level, experience), rname = rname, coupons = coupons, rid = rid, achievements = achievements)
    else:
        return redirect(url_for('home_page.home'))



@search_page.route('/couponOffers<rid>.html', methods=['GET', 'POST'])
@search_page.route('/couponOffers<rid>', methods=['GET', 'POST'])
def couponOffers(rid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home_page.home'))

    restaurant = get_resturant_by_rid(rid)
    if restaurant:
        rname = get_restaurant_name_by_rid(rid)
        coupons = filter_valid_coupons(get_coupons(rid))
        points = get_points(session['account'], rid).points
        if 'cid' in request.form:
            cid = request.form['cid']
            c = get_coupon_by_cid(cid)
            if c['points'] <= points:
                update_points(session['account'], rid, (-1 * c['points']))
                insert_redeemed_coupon(cid, session['account'], rid)
                points = get_points(session['account'], rid).points
                return render_template("couponOffers.html", rid = rid, rname = rname, coupons = coupons, points = points, bought = c['cname'])
            else:
                return render_template("couponOffers.html", rid = rid, rname = rname, coupons = coupons, points = points, errmsg = ["You do not have enough points for this coupon"])

        return render_template("couponOffers.html", rid = rid, rname = rname, coupons = coupons, points = points)
    else:
        return redirect(url_for('home_page.home'))

@search_page.route('/<filter>Achievements<rid>.html', methods=['GET', 'POST'])
@search_page.route('/<filter>Achievements<rid>', methods=['GET', 'POST'])
def restaurantAchievements(rid, filter):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home_page.home'))

    switcher = {
        "available": NOT_STARTED,
        "inProgress" : IN_PROGRESS,
        "complete" : COMPLETE
    }

    # Check that filter is valid
    if switcher.get(filter, -1) == -1:
        return redirect(url_for('home_page.home'))

    restaurant = get_resturant_by_rid(rid)
    if restaurant:
        rname = get_restaurant_name_by_rid(rid)
        # Gets achievements
        achievements = get_achievements_with_progress_data(get_achievements_by_rid(rid), session['account'])
        return render_template("restaurantAchievements.html", rid = rid, rname = rname, achievements = achievements, filterID = switcher.get(filter))
    else:
        return redirect(url_for('home_page.home'))
