###################################################
#                                                 #
#   Includes all routes to profile pages.         #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
profile_page = Blueprint('profile_page', __name__, template_folder='templates')
from databaseHelpers.user import *

@profile_page.route('/profile.html')
@profile_page.route('/profile')
def profile():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))
    else:
        user = get_user(session['account'])
        return render_template('profile.html', user = user)
