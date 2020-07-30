###################################################
#                                                 #
#   Includes all routes to using a coupon pages.  #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from helpers.qr_code import *

qr_page = Blueprint('qr_page', __name__, template_folder='templates')

@qr_page.route('/scanFailure.html')
@qr_page.route('/scanFailure')
def scan_failure():
    return render_template('scanFailure.html')


@qr_page.route('/scanSuccessful.html')
@qr_page.route('/scanSuccessful')
def scan_successful():
    return render_template('scanSuccessful.html')


@qr_page.route('/scanNoCoupon.html')
@qr_page.route('/scanNoCoupon')
def scan_no_coupon():
    return render_template('scanNoCoupon.html')
