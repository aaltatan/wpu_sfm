from flask import Blueprint, request
from ... import db
from ...models import Faculty, Service
from typing import List
from ...utils import login_required
from icecream import ic

api = Blueprint("api", __name__, url_prefix='/api')


@api.route("/faculties")
@login_required
def get_faculties():
    faculties: List[Faculty] = Faculty.query.all()
    faculties = [{"id": fac.id, "value": fac.title} for fac in faculties]
    return {"result": faculties}


@api.route("/services")
@login_required
def get_services():
    services: List[Service] = Service.query.order_by(Service.name).all()
    services = [{"id": service.id, "value": service.name, "price": service.price}
                for service in services]
    return {"result": services}
