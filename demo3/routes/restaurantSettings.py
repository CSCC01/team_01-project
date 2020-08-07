###################################################
#                                                 #
#   Includes all routes to registration pages.    #
#   This currently includes customer, employee,   #
#   and owner registration.                       #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.threshold import *
from databaseHelpers.restaurant import *
from databaseHelpers.employee import *

settings_page = Blueprint('setting_page', __name__, template_folder='templates')

# The registration options page
@settings_page.route('/restaurantSettings.html', methods=['GET', 'POST'])
@settings_page.route('/restaurantSettings', methods=['GET', 'POST'])
def settings():
    # If someone is already logged in they get redirected to the home page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    elif session['type'] != 1 and session['type'] != 2:
        return redirect(url_for('home_page.home'))

    else:
        errmsg = []
        if session['type'] == 1:
            rid = get_rid(session['account'])
        elif session['type'] == 2:
            rid = get_employee_rid(session["account"])
        update = None
        if request.method == 'POST':
            if 'delete' in request.form:
                level = request.form['level']
                delete_threshold(rid, level)
            elif 'update' in request.form:
                update = int(request.form['level'])
            elif 'add' in request.form:
                level = request.form['level']
                reward = request.form['points']
                if check_threshold(rid, level):
                    errmsg = update_threshold(rid, level, reward)
                else:
                    errmsg = insert_threshold(rid, level, reward)
            elif 'update_reward' in request.form:
                level = request.form['level_update']
                reward = request.form['points_update']
                if check_threshold(rid, level):
                    errmsg = update_threshold(rid, level, reward)
        threshold_list = get_thresholds(rid)
        return render_template('restaurantSettings.html', thresholds = threshold_list, errmsg = errmsg, update = update)
