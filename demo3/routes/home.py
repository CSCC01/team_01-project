###################################################
#                                                 #
#   Includes all routes to home pages.            #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint

home_page = Blueprint('home_page', __name__, template_folder='templates')


# The home landing page
# Currently nothing is here
@home_page.route('/home')
@home_page.route('/home.html')
def home():
    if 'account' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login_page.login'))
