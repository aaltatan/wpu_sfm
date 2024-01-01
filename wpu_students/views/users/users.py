from ...utils import login_required, admin_required, flash, redirect, url_for
from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
from .schemas import AddUser, EditUser
from pydantic import ValidationError
from ...models import User
from ... import db


users = Blueprint('users', __name__, url_prefix="/users")


@users.route("/")
@login_required
@admin_required
def show_users():
    users = User.query.filter(User.role != 'admin').all()
    return render_template("users/show_users.html",
                           users=users)


@users.route("/add", methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == "POST":
        try:
            new_user = AddUser(**request.form.to_dict())
        except ValidationError as err:
            for e in err.errors():
                message = e['loc'][0] + " " + e["msg"]
                flash(message, category="danger")
                return redirect(url_for("users.add_user"))

        user_exists = User.query.filter_by(
            username=new_user.username).first()
        if user_exists:
            flash(f"{new_user.username} does already exists", category='danger')
            return redirect(url_for("users.add_user"))

        new_user.password = generate_password_hash(new_user.password,
                                                   method="pbkdf2")
        new_user = new_user.model_dump()
        user = User(**new_user)
        db.session.add(user)
        db.session.commit()
        flash(f"{new_user['username']} has been created successfully",
              category='success')
        return redirect(url_for("users.show_users"))

    return render_template("users/add_user.html")


@users.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id: int):

    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        flash(f"user does not exist", category='danger')
        return redirect(url_for("users.edit_user", id=user_exists.id))

    if request.method == "POST":
        try:
            edit_user = EditUser(**request.form.to_dict())
        except ValidationError as err:
            for e in err.errors():
                message = e['loc'][0] + " " + e["msg"]
                flash(message, category="danger")
                return redirect(url_for("users.edit_user", id=user_exists.id))

        filt = User.username == edit_user.username
        username_exists = User.query.filter(filt, User.id != id).first()

        if username_exists:
            flash(f"{edit_user.username} does already exist", category='danger')
            return redirect(url_for("users.edit_user", id=user_exists.id))

        user_exists.username = edit_user.username
        user_exists.fullname = edit_user.fullname

        db.session.commit()

        flash(f"{edit_user.username} has been updated successfully",
              category='success')
        return redirect(url_for("users.show_users"))

    return render_template("users/edit_user.html",
                           user=user_exists)


@users.route("/delete/<int:id>")
@login_required
@admin_required
def delete_user(id: int):
    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        flash(f"user does not exist", category='danger')
        return redirect(url_for("users.show_users"))

    db.session.delete(user_exists)
    db.session.commit()
    flash(f"{user_exists.username} has been deleted successfully",
          category='success')
    return redirect(url_for("users.show_users"))


@users.route("/deactivate/<int:id>")
@login_required
@admin_required
def deactivate_user(id: int):
    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        flash(f"user does not exist", category='danger')
        return redirect(url_for("users.show_users"))

    user_exists.is_activated = False
    db.session.commit()
    flash(f"{user_exists.username} has been deactivated successfully",
          category='success')
    return redirect(url_for("users.show_users"))


@users.route("/activate/<int:id>")
@login_required
@admin_required
def activate_user(id: int):
    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        flash(f"user does not exist", category='danger')
        return redirect(url_for("users.show_users"))

    user_exists.is_activated = True
    db.session.commit()
    flash(f"{user_exists.username} has been activated successfully",
          category='success')
    return redirect(url_for("users.show_users"))


@users.route("/reset/<int:id>")
@login_required
@admin_required
def reset_user(id: int):
    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        flash(f"user does not exist", category='danger')
        return redirect(url_for("users.show_users"))

    user_exists.password = generate_password_hash("12345678", method="pbkdf2")
    db.session.commit()
    flash(f"{user_exists.username}'s Password has been reset successfully",
          category='success')
    return redirect(url_for("users.show_users"))
