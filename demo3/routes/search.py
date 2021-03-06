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
from databaseHelpers.qr_code import *
from databaseHelpers.achievement import *
from databaseHelpers.achievementProgress import *
from databaseHelpers.redeemedCoupons import *
from databaseHelpers.points import *
from databaseHelpers.experience import *
from databaseHelpers.level import *
from databaseHelpers.threshold import *
from databaseHelpers.leaderboard import *
from databaseHelpers.favourite import *
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

# Referenced from
# https://stackoverflow.com/questions/28229668/python-flask-how-to-get-route-id-from-url
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
        ### TODO: get likes
        if "loved" in request.form:
            add_favourite(session['account'], rid)

        elif "unloved" in request.form:
            remove_faviourite(session['account'], rid)

        liked = check_favourite(session['account'], rid)

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
        milestone = get_milestone(uid, rid)
        threshold_list = get_incomplete_milestones(rid, level)[:3]
        points = get_points(session['account'], rid).points
        return render_template("restaurant.html", restaurant = restaurant, level = level,
                                overflow = get_experience_since_last_level(level, experience),
                                rname = rname, coupons = coupons, rid = rid, achievements = achievements,
                                milestone = milestone, liked = liked, thresholds = threshold_list, points = points)
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
        coupons.sort(key=lambda x: x.get('level'))
        points = get_points(session['account'], rid).points
        level = convert_experience_to_level(get_experience(session['account'], rid).experience)
        filter = "all"
        if 'cid' in request.form:
            cid = request.form['cid']
            c = get_coupon_by_cid(cid)
            errmsg = []

            # if meet all the requirement
            if c['points'] <= points and c['clevel'] <= level:
                update_points(session['account'], rid, (-1 * c['points']))
                insert_redeemed_coupon(cid, session['account'], rid)
                points = get_points(session['account'], rid).points
                return render_template("couponOffers.html", rid = rid, rname = rname, coupons = coupons, points = points, level = level, bought = c['cname'], filter = filter)

            # not enough points
            if c['points'] > points:
                errmsg.append("You do not have enough points for this coupon.")

            # not enough level
            if c['clevel'] > level:
                errmsg.append("You do not have high enough level to purchase this coupon.")

            return render_template("couponOffers.html", rid = rid, rname = rname, coupons = coupons, points = points, level = level, errmsg = errmsg, filter = filter)
        elif request.method == 'POST' and 'purchasable' in request.form:
            filter = "purchasable"
        elif request.method == 'POST' and 'notpurchasable' in request.form:
            filter = "notpurchasable"
        return render_template("couponOffers.html", rid = rid, rname = rname, coupons = coupons, points = points, level = level, filter = filter)
    else:
        return redirect(url_for('home_page.home'))

@search_page.route('/availableAchievements<rid>.html', methods=['GET', 'POST'])
@search_page.route('/availableAchievements<rid>', methods=['GET', 'POST'])
def restaurantAchievements(rid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home_page.home'))

    restaurant = get_resturant_by_rid(rid)
    if restaurant:
        filter = "all"
        if request.method == 'POST' and 'update' in request.form:
            aid = request.form['achievement']
            uid = session['account']
            imgurl = update_achievement_qr("http://127.0.0.1:5000/verifyAchievement/"+str(aid)+"/"+str(uid), aid, uid)
            achievement = get_achievement_with_progress_data(aid, uid)
            return render_template("achievementQR.html", imgurl=imgurl, rid=rid, a=achievement)
        elif request.method == 'POST' and 'available' in request.form:
            filter = "available"
        elif request.method == 'POST' and 'in_progress' in request.form:
            filter = "in_progress"
        elif request.method == 'POST' and 'completed' in request.form:
            filter = "completed"
        rname = get_restaurant_name_by_rid(rid)
        # Gets achievements
        achievements = get_achievements_with_progress_data(get_achievements_by_rid(rid), session['account'])
        return render_template("restaurantAchievements.html", rid = rid, rname = rname, achievements = achievements, filter = filter)
    else:
        return redirect(url_for('home_page.home'))


@search_page.route('/milestones<rid>.html', methods=['GET', 'POST'])
@search_page.route('/milestones<rid>', methods=['GET', 'POST'])
def milestones(rid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to customers only, if user is not a customer, redirect to home page
    elif session['type'] != -1:
        return redirect(url_for('home_page.home'))

    restaurant = get_resturant_by_rid(rid)
    if restaurant:
        rname = get_restaurant_name_by_rid(rid)
        filter = "all"
        if request.method == 'POST' and 'all' in request.form:
            filter = "all"
        elif request.method == 'POST' and 'complete' in request.form:
            filter = "complete"
        elif request.method == 'POST' and 'incomplete' in request.form:
            filter = "incomplete"

        uid = session["account"]
        experience = get_experience(uid, rid).experience
        level = convert_experience_to_level(experience)
        threshold_list = get_thresholds(rid)
        return render_template("milestones.html", rid = rid, thresholds = threshold_list, level = level, filter = filter, rname=rname)
    else:
        return redirect(url_for('home_page.home'))


# View customer leader board
@search_page.route('/leaderBoard<rid>', methods=['GET', 'POST'])
def leaderBoard(rid):
    rname = get_restaurant_name_by_rid(rid)
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    if session["type"] == -1:
        leaderBoard_list  = top_n_in_order(rid, 10)
        lbs = get_data(leaderBoard_list)

        return render_template("leaderBoard.html", rid=rid, lbs=lbs, rname=rname)
    else:
        return redirect(url_for('home_page.home'))
