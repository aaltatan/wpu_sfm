from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash
from datetime import timedelta


class Base(DeclarativeBase):
    ...


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hello World!"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wpu.db'
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    db.init_app(app)

    app.add_template_filter(lambda x: f'{x:,}', "currency")

    from .views.dashboard.dashboard import dashboard
    from .views.auth.auth import auth
    from .views.users.users import users
    from .views.settings.faculties import faculties
    from .views.settings.services import services
    from .views.receipts.receipts import receipts
    from .views.api.api import api

    app.register_blueprint(dashboard)
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(faculties)
    app.register_blueprint(services)
    app.register_blueprint(receipts)
    app.register_blueprint(api)

    from .models import User, Faculty, Service, Receipt, ReceiptDetail

    with app.app_context():
        db.create_all()
        admin_exists = User.query.filter_by(role='admin').first()
        if not admin_exists:
            admin = {"username": "admin",
                     "fullname": "administrator",
                     "password": generate_password_hash("Qazasd@123", method="pbkdf2"),
                     "is_activated": True,
                     "role": "admin"}
            admin = User(**admin)
            db.session.add(admin)
            db.session.commit()

    return app
