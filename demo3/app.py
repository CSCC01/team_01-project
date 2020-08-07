# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from models import db
from datetime import date
import config
import os
import hashlib
import re

from routes.registration import registration_page
from routes.coupon import coupon_page
from routes.achievement import achievement_page
from routes.qrCode import qr_page
from routes.home import home_page
from routes.employee import employee_page
from routes.profile import profile_page
from routes.search import search_page
from routes.login import login_page
from routes.restaurant import restaurant_page
from routes.leaderboard import leaderboard_page

app = Flask(__name__)
app.register_blueprint(registration_page)
app.register_blueprint(coupon_page)
app.register_blueprint(achievement_page)
app.register_blueprint(home_page)
app.register_blueprint(employee_page)
app.register_blueprint(profile_page)
app.register_blueprint(search_page)
app.register_blueprint(login_page)
app.register_blueprint(qr_page)
app.register_blueprint(restaurant_page)
app.register_blueprint(leaderboard_page)
app.secret_key = 'shhhh'

app.config.from_object(config)

db.init_app(app)

if __name__ == '__main__':
    app.run()
