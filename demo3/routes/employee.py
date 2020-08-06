###################################################
#                                                 #
#   Includes all routes to employee pages.        #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.restaurant import *
from databaseHelpers.employee import *
from databaseHelpers.user import *

employee_page = Blueprint('employee_page', __name__, template_folder='templates')

@employee_page.route('/employee.html', methods=['GET', 'POST'])
@employee_page.route('/employee', methods=['GET', 'POST'])
def employee():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] == -1 or session["type"] == 0:
        return redirect(url_for('home_page.home'))

    filter = 1
    if request.method == 'POST':
        if "delete" in request.form:
            delete_employee(request.form['user'])
            uid = request.form['user']
        elif "promote" in request.form:
            update_type(uid, 2)
            uid = request.form['user']
        elif "depromote" in request.form:
            update_type(uid, 0)
            uid = request.form['user']
        elif "general" in request.form:
            filter = 0
        elif "manager" in request.form:
            filter = 2



    if session["type"] == 1:
        rid = get_rid(session["account"])
    elif session["type"] == 2:
        rid = get_employee_rid(session["account"])

    employee_list = get_employees(rid)
    return render_template("employee.html", employees = employee_list, filter = filter)
