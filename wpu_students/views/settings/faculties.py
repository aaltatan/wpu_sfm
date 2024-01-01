from flask import Blueprint, render_template, request, redirect, url_for, flash
from ...utils import login_required, admin_required
from ...models import Faculty
from ... import db

faculties = Blueprint('faculties',
                      __name__,
                      url_prefix="/settings/faculties")


@faculties.route("/")
@login_required
def show_faculties():
    faculties_list = Faculty.query.order_by(Faculty.title).all()
    return render_template("settings/faculties.html",
                           faculties=faculties_list)


@faculties.route("/add", methods=['POST', 'GET'])
@login_required
def add_faculty():
    if request.method == "POST":
        faculty_title = request.form.get("title")
        if not faculty_title:
            flash("Faculty title is required", category='danger')
            return redirect(url_for('faculties.show_faculties'))

        faculty = Faculty(title=faculty_title)
        db.session.add(faculty)
        db.session.commit()

        flash(f"{faculty_title} has been added successfully", category='success')

    return redirect(url_for('faculties.show_faculties'))


@faculties.route("/edit/<int:id>", methods=['POST', 'GET'])
@login_required
def edit_faculty(id: int):

    if request.method == "POST":

        faculty_exists = Faculty.query.filter_by(id=id).first()
        if not faculty_exists:
            flash("There is no such faculty like this", category='danger')
            return redirect(url_for('faculties.show_faculties'))

        faculty_title = request.form.get("title")
        if not faculty_title:
            flash("Faculty title is required", category='danger')
            return redirect(url_for('faculties.show_faculties'))

        faculty_exists.title = faculty_title
        db.session.commit()

        flash(f"{faculty_title} has been updated successfully",
              category='success')

    return redirect(url_for('faculties.show_faculties'))


@faculties.route("/delete/<int:id>")
@login_required
@admin_required
def delete_faculty(id: int):

    faculty_exists = Faculty.query.filter_by(id=id).first()

    if not faculty_exists:
        flash("There is no such faculty like this", category='danger')
        return redirect(url_for('faculties.show_faculties'))

    db.session.delete(faculty_exists)
    db.session.commit()

    flash(f"{faculty_exists.title} has been deleted successfully",
          category='success')

    return redirect(url_for('faculties.show_faculties'))
