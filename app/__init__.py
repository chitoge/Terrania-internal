from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from config import config


db = SQLAlchemy()
ma = Marshmallow()


def make_json_error(ex):
    return_code = (ex.code
                    if isinstance(ex, HTTPException)
                    else 500)
    response = jsonify(status=return_code, message=str(ex))
    response.status_code = return_code
    return response


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    ma.init_app(app)

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api')

    #app.errorhandler(Exception)(make_json_error)
    #app.errorhandler(HTTPException)(make_json_error)

    return app
