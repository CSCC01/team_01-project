###################################################
#                                                 #
#   Includes all routes to employee pages.        #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.restaurant import *
from databaseHelpers.employee import *

employee_page = Blueprint('employee_page', __name__, template_folder='templates')

@employee_page.route('/employee.html', methods=['GET', 'POST'])
@employee_page.route('/employee', methods=['GET', 'POST'])
def employee():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home_page.home'))

    if request.method == 'POST':
        uid = request.form['user']
        delete_employee(request.form['user'])

    rid = get_rid(session["account"])
    employee_list = get_employees(rid)

    return render_template("employee.html", employees = employee_list)
