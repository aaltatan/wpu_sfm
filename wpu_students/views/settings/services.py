from flask import Blueprint, redirect, render_template, url_for, request, flash
from ...utils import login_required, admin_required
from pydantic import ValidationError
from .schemas import ServiceSchema
from ...models import Service
from ... import db


services = Blueprint("services",
                     __name__,
                     url_prefix="/settings/services")


@services.route("/")
@login_required
def show_services():
    services = Service.query.all()
    return render_template("settings/services.html",
                           services=services)


@services.route("/add", methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == "POST":
        try:
            new_service = ServiceSchema(**request.form.to_dict())
        except ValidationError as err:
            for e in err.errors():
                flash(e["loc"][0] + e["msg"], category='danger')
                return redirect(url_for("services.show_services"))

        service_name_exists = Service.query.filter_by(
            name=new_service.name).first()

        if service_name_exists:
            flash(f"{new_service.name} does already exists", 'danger')
            return redirect(url_for("services.show_services"))

        new_service = Service(**new_service.model_dump())
        db.session.add(new_service)
        db.session.commit()
        flash(f"{new_service.name} has been added successfully", "success")

    return redirect(url_for('services.show_services'))


@services.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_service(id: int):
    if request.method == "POST":
        try:
            edit_service = ServiceSchema(**request.form.to_dict())
        except ValidationError as err:
            for e in err.errors():
                flash(e["loc"][0] + " " + e["msg"], category='danger')
                return redirect(url_for("services.show_services"))

        service_exists = Service.query.filter_by(id=id).first()
        if not service_exists:
            flash(f"Service does not exist", 'danger')
            return redirect(url_for("services.show_services"))

        filt1 = Service.id != id
        filt2 = Service.name == edit_service.name
        service_name_exists = Service.query.filter(filt1, filt2).first()
        if service_name_exists:
            flash(f"{edit_service.name} does already exists", 'danger')
            return redirect(url_for("services.show_services"))

        service_exists.name = edit_service.name
        service_exists.price = edit_service.price
        db.session.commit()
        flash(f"{edit_service.name} has been updated successfully", "success")

    return redirect(url_for('services.show_services'))


@services.route("/delete/<int:id>")
@login_required
@admin_required
def delete_service(id: int):
    service_exists = Service.query.filter_by(id=id).first()
    if not service_exists:
        flash(f"Service does not exist", 'danger')
        return redirect(url_for("services.show_services"))

    db.session.delete(service_exists)
    db.session.commit()
    flash(f"{service_exists.name} has been deleted successfully", "success")

    return redirect(url_for('services.show_services'))
