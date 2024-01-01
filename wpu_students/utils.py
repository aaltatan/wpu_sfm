import functools
from flask import redirect, url_for, g, flash, request


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user.get("is_activated") == False:
            flash("You need to login first", category="info")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.get('role') != 'admin':
            flash("this is restricted area", category="danger")
            return redirect(request.referrer)

        return view(**kwargs)

    return wrapped_view
