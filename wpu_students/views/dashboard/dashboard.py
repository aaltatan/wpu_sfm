from flask import Blueprint, render_template, request, make_response, url_for, redirect
from ...utils import login_required
from datetime import timedelta


dashboard = Blueprint('dashboard', __name__)


@dashboard.route("/")
@login_required
def index():
    return render_template("dashboard/dashboard.html")


@dashboard.route("/set_theme")
def set_theme():
    current_theme = request.cookies.get("theme")
    response = make_response()

    criteria = 'dark' if current_theme == "light" else 'light'
    response.set_cookie('theme',
                        criteria,
                        timedelta(days=365))

    response.headers['location'] = request.referrer

    return response, 302
