from flask import Flask

from routes.medicine import app as medicine_app
from routes.pharmacy import app as pharmacy_app
from routes.inventory import app as inventory_app


def register_all_blueprint(app: Flask):

    app.register_blueprint(medicine_app)
    app.register_blueprint(pharmacy_app)
    app.register_blueprint(inventory_app)
