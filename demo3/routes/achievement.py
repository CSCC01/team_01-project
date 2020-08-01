###################################################
#                                                 #
#   Includes all routes to achievement page.      #
#   This includes my achievements and create an   #
#   achievement.                                  #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.achievement import *
from databaseHelpers.restaurant import *

achievement_page = Blueprint('achievement_page', __name__, template_folder='templates')

@achievement_page.route('/achievement.html', methods=['GET', 'POST'])
@achievement_page.route('/achievement', methods=['GET', 'POST'])
def achievement():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home_page.home'))

    else:
        if request.method == 'POST':
            aid = request.form['achievement']
            delete_achievement(aid)
    #get achievements
    rid = get_rid(session["account"])
    delete_expired_achievements(rid)
    achievement_list = get_achievements_by_rid(rid)

    return render_template("achievement.html", achievements = achievement_list)


# To create an achievement
@achievement_page.route('/createAchievement.html', methods=['GET', 'POST'])
@achievement_page.route('/createAchievement', methods=['GET', 'POST'])
def create_achievement():
    # If someone is not logged in redirects them to login page, same as coupon
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home_page.home'))

    if request.method == 'POST':
        rid = get_rid(session["account"])
        name = request.form['name']
        experience = request.form['experience']
        points = request.form['points']
        type = int(request.form.get('type'))
        item = request.form['item']
        amount = request.form['amount' + str(type)]
        end = request.form['end']
        begin = request.form['start']
        indefinite = "indefinite" in request.form

        value = item + ";" + amount + ";" + str(indefinite) + ";" + begin + ";" + end

        errmsg = get_errmsg(name, experience, points, type, value)

        if not errmsg:
            insert_achievement(rid, name, experience, points, type, value)
            return redirect(url_for('achievement_page.achievement'))
        else:
            return render_template('createAchievement.html', errmsg = errmsg)

    return render_template('createAchievement.html')