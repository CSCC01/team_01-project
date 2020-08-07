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
from databaseHelpers.experience import *
from databaseHelpers.level import *

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
            coupon = get_coupon_by_cid(cid)
            rname = find_res_name_of_coupon_by_cid(cid)
            raddr = find_res_addr_of_coupon_by_cid(cid)
            ulevel = convert_experience_to_level(get_experience(uid, coupon.get("rid")).experience)
            # imgurl = to_qr("https://pickeasy-beta.herokuapp.com/useCoupon/"+str(cid))
            imgurl = to_qr("http://127.0.0.1:5000/useCoupon/"+str(uid)+"/"+str(cid), uid, cid)
            return render_template("couponQR.html", imgurl=imgurl, name=coupon.get("cname"), description=coupon.get("cdescription"), 
                                                    points=coupon.get("points"), level=coupon.get("clevel"), ulevel=ulevel, 
                                                    begin=coupon.get("begin"), expiration=coupon.get("expiration"),
                                                    rname=rname, raddr=raddr)

        coupons = get_redeemed_coupons_by_uid(session["account"])
        return render_template("coupon.html", coupons = coupons)

    else:
        if request.method == 'POST':
            cid = request.form['coupon']
            delete_coupon(cid)
        if session["type"] == 1:
            rid = get_rid(session["account"])
        else:
            rid = get_employee_rid(session["account"])
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
    elif session['type'] == -1 or session["type"] == 0:
        return redirect(url_for('home_page.home'))

    errmsg = []

    if request.method == 'POST':
        # Grabs information from coupon fields
        name = request.form['name']
        points = request.form['points']
        description = request.form['description']
        level = request.form['level']
        expiration = request.form['end']
        begin = request.form['begin']
        # true -> no expiration date, false -> expiration date required
        indefinite = "indefinite" in request.form

        if session["type"] == 1:
            rid = get_rid(session["account"])
        else:
            rid = get_employee_rid(session["account"])
        errmsg = insert_coupon(rid, name, points, description, level, begin, expiration, indefinite)

        # Inserting was successful
        if not errmsg:
            return redirect(url_for('coupon_page.coupon'))

        # Inserting failed
        return render_template('createCoupon.html', errmsg = errmsg,
                            info = {'name': name, 'points': points, 'description': description, 'level': level, 'expiration': expiration, 'begin': begin})

    return render_template('createCoupon.html')


# View customer coupons
@coupon_page.route('/couponStats.html', methods=['GET', 'POST'])
@coupon_page.route('/couponStats', methods=['GET', 'POST'])
def couponStats():
    today = date.today()
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] == -1 or session["type"] == 0:
        return redirect(url_for('home_page.home'))

    elif session['type'] == 1:
        rid = get_rid(session['account'])
    else:
        rid = get_employee_rid(session["account"])

    filter = "all"
    if request.method == 'POST' and "deleted" in request.form:
        filter = "deleted"
    elif request.method == 'POST' and "expired" in request.form:
        filter = "expired"
    elif request.method == 'POST' and "active" in request.form:
        filter = "active"

    coupon_list = get_redeemed_coupons_by_rid(rid)
    return render_template("couponStats.html", coupons = coupon_list, today = today, filter = filter)


@coupon_page.route('/useCoupon/<uid>/<cid>', methods=['GET', 'POST'])
def use_coupon(cid,uid):
    scanner = session['account']
    rid = get_rid_by_cid(cid)
    access = verify_scan_list(rid)
    rname = get_restaurant_name_by_rid(rid)
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to employee/owner only, if user is a customer, redirect to home page
    elif session['type'] == -1 or scanner not in access:
        return redirect(url_for('qr_page.scan_failure', rname=rname))

    # find rcid
    rcid = find_rcid_by_cid_and_uid(cid, uid)
    if rcid != "Not Found":
        coupon = get_coupon_by_cid(cid)
        
        # check if it is before coupon start date or after coupon end date
        if coupon["status"] != 0:
            return redirect(url_for('qr_page.scan_forbidden', forbiddenType = coupon["status"], itemType = 'Coupon'))
        
        # mark used
        mark_redeem_coupon_used_by_rcid(rcid)
        return redirect(url_for('qr_page.scan_successful'))
    return redirect(url_for('qr_page.scan_nonexistent', scanType = 0))
