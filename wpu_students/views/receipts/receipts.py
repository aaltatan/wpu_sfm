from flask import Blueprint, redirect, url_for, flash, request, render_template, jsonify, session
from ...models import Receipt, Faculty, Service, ReceiptDetail
from pydantic import ValidationError
from ...utils import login_required
from .schemas import ReceiptSchema
from sqlalchemy import text, desc
from .queries import queries
from icecream import ic
from ... import db
import itertools
from functools import reduce
import json


receipts = Blueprint("receipts",
                     __name__,
                     url_prefix="/receipts")


@receipts.route("/")
@login_required
def show_receipts():
    # handling pagination
    PER_PAGE = 10
    current_page = int(request.args.get('page', 0))
    if current_page < 0:
        return redirect(url_for('receipts.show_receipts'))

    params = {"user_id": session.get('current_user')['id']}
    receipts = db.session.execute(statement=text(queries['default']),
                                  params=params)
    receipts = receipts.mappings().all()
    batches = list(itertools.batched(receipts, PER_PAGE))

    # handling pagination
    if current_page >= len(batches):
        return redirect(url_for('receipts.show_receipts'))
    selected_batch = batches[current_page]

    return render_template("receipts/receipts.html",
                           batches=batches,
                           selected_batch=selected_batch)


@receipts.route("/add", methods=['GET', 'POST'])
@login_required
def add_receipt():
    data = {
        "faculties": Faculty.query.all(),
        "services": Service.query.all()
    }
    if request.method == "POST":
        try:
            receipt = ReceiptSchema(**request.get_json()).model_dump()
        except ValidationError as err:
            errors = [{'loc': i['loc'][0], 'msg': i['msg']}
                      for i in err.errors()]
            ic(errors)
            return jsonify(errors), 400
        rows = receipt.pop('rows')

        new_receipt = Receipt(**receipt)
        db.session.add(new_receipt)
        db.session.commit()

        last_id = Receipt.query.order_by(desc(Receipt.id)).first()
        for row in rows:
            new_row = ReceiptDetail(**row, receipt_id=last_id.id)
            db.session.add(new_row)

        db.session.commit()

        return jsonify("Data is saved"), 201

    return render_template('receipts/add_receipts.html', **data)
