###################################################
#                                                 #
#   Includes all routes to coupon page. This      #
#   currently my coupon, create coupon, view      #
#   user coupon pages and use coupon.             #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint

coupon_page = Blueprint('coupon_page', __name__, template_folder='templates')
from databaseHelpers.coupon import *
from databaseHelpers.employee import *
from databaseHelpers.redeemedCoupons import *
from databaseHelpers.qr_code import *

# My coupon page
@coupon_page.route('/coupon.html', methods=['GET', 'POST'])
@coupon_page.route('/coupon', methods=['GET', 'POST'])
def coupon():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    ### Customer viewing of coupons
    elif session["type"] == -1:
        if request.method == 'POST':
            cid = request.form['coupon']
            uid = session['account']
            rcid = find_rcid_by_cid_and_uid(cid,uid)
            # imgurl = to_qr("https://pickeasy-beta.herokuapp.com/useCoupon/"+str(cid))
            imgurl = to_qr("http://127.0.0.1:5000/useCoupon/"+str(cid)+"/"+str(uid), rcid)
            return render_template("couponQR.html", imgurl=imgurl)

        coupons = get_redeemed_coupons_by_uid(session["account"])
        return render_template("coupon.html", coupons = coupons)

    # Employee view of coupon page
    if session["type"] == 0:
        rid = get_employee_rid(session["account"])
        coupon_list = get_coupons(rid)
        return render_template("coupon.html", coupons = coupon_list)

    # Owners view of coupon page
    else:
        if request.method == 'POST':
            cid = request.form['coupon']
            delete_coupon(cid)

        rid = get_rid(session["account"])
        coupon_list = get_coupons(rid)
        return render_template("coupon.html", coupons = coupon_list)


# Create a coupon page
@coupon_page.route('/createCoupon.html', methods=['GET', 'POST'])
@coupon_page.route('/createCoupon', methods=['GET', 'POST'])
def create_coupon():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home_page.home'))

    errmsg = []

    if request.method == 'POST':
        # Grabs information from coupon fields
        name = request.form['name']
        points = request.form['points']
        description = request.form['description']
        expiration = request.form['end']
        begin = request.form['begin']
        # true -> no expiration date, false -> expiration date required
        indefinite = "indefinite" in request.form

        rid = get_rid(session["account"])
        errmsg = insert_coupon(rid, name, points, description, begin, expiration, indefinite)

        # Inserting was successful
        if not errmsg:
            return redirect(url_for('coupon_page.coupon'))

        # Inserting failed
        return render_template('createCoupon.html', errmsg = errmsg,
                            info = {'name': name, 'points': points, 'description': description, 'expiration': expiration, 'begin': begin})

    return render_template('createCoupon.html')


# View customer coupons
@coupon_page.route('/viewUserCoupons.html', methods=['GET', 'POST'])
@coupon_page.route('/viewUserCoupons', methods=['GET', 'POST'])
def viewUserCoupons():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home_page.home'))

    rid = get_rid(session['account'])
    coupon_list = get_redeemed_coupons_by_rid(rid)
    today = date.today()
    return render_template("viewUserCoupons.html", coupons = coupon_list, today = today)


@coupon_page.route('/useCoupon/<cid>/<uid>', methods=['GET', 'POST'])
def use_coupon(cid,uid):
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to employee/owner only, if user is a customer, redirect to home page
    elif session['type'] == -1:
        return redirect(url_for('qr_page.scan_failure'))

    # find rcid
    rcid = find_rcid_by_cid_and_uid(cid, uid)
    if rcid != "Not Found":
        # mark used
        mark_redeem_coupon_used_by_rcid(rcid)
        return redirect(url_for('qr_page.scan_successful'))
    return redirect(url_for('qr_page.scan_no_coupon'))
