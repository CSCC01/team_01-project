###################################################
#                                                 #
#   Includes all routes to using a coupon pages.  #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.qr_code import *

qr_page = Blueprint('qr_page', __name__, template_folder='templates')

@qr_page.route('/scanFailure.html')
@qr_page.route('/scanFailure')
def scan_failure():
    return render_template('scanFailure.html')


@qr_page.route('/scanSuccessful.html')
@qr_page.route('/scanSuccessful')
def scan_successful():
    return render_template('scanSuccessful.html')


@qr_page.route('/scanNonexistent<scanType>.html')
@qr_page.route('/scanNonexistent<scanType>')
def scan_nonexistent(scanType):
    return render_template('scanNonexistent.html', scanType = scanType)
