from flask import Blueprint, render_template, request, session, url_for, redirect, flash, g
from werkzeug.security import check_password_hash
from ...models import User
from .schemas import UserLogin
from pydantic import ValidationError
from ...utils import login_required


auth = Blueprint("auth", __name__)


@auth.before_app_request
def load_logged_in_user():
    current_user = session.get('current_user')
    if current_user is None:
        g.user = None
    else:
        g.user = current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user_login = UserLogin(**request.form)
        except ValidationError as err:
            for e in err.errors():
                message = e['loc'][0] + " " + e["msg"]
                flash(message, category="danger")
                return redirect(url_for("auth.login"))

        user_exists = User.query.filter_by(username=user_login.username,
                                           is_activated=True).first()

        if user_exists:
            if not check_password_hash(user_exists.password, user_login.password):
                flash("invalid credentials!!!", category='danger')
                return redirect(url_for("auth.login"))
            else:
                session.clear()
                user = {"id": user_exists.id,
                        "username": user_exists.username,
                        "fullname": user_exists.fullname,
                        "role": user_exists.role,
                        "is_activated": user_exists.is_activated}
                session['current_user'] = user
                flash(f"Welcome {user_exists.fullname}", category="success")
                return redirect(url_for('dashboard.index'))
        else:
            flash("invalid credentials!!!", category='danger')
            return redirect(url_for("auth.login"))

    return render_template('auth/login.html')


@auth.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
