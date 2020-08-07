from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.leaderboard import *
from databaseHelpers.experience import *
from databaseHelpers.level import *
from databaseHelpers.employee import *
from databaseHelpers.restaurant import *

leaderboard_page = Blueprint('leaderboard_page', __name__, template_folder='templates')

@leaderboard_page.route('/leaderBoard.html', methods=['GET', 'POST'])
@leaderboard_page.route('/leaderBoard', methods=['GET', 'POST'])
def leaderboard():
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    elif session["type"] == -1 or session["type"] == 0:
        return redirect(url_for('home_page.home'))

    if session["type"] == 1:
        rid = get_rid(session["account"])
    elif session["type"] == 2:
        rid = get_employee_rid(session["account"])

    rname = get_restaurant_name_by_rid(rid)
    leaderBoard_list  = top_n_in_order(rid, 10)
    lbs = get_data(leaderBoard_list)
    return render_template("leaderBoard.html", rid=rid, lbs=lbs, rname=rname)
