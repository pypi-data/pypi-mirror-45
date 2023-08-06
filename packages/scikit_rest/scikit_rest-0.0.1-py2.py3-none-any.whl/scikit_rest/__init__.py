"""Automatically serve ML model as a REST API"""
__version__ = "0.0.1"

from flask import Flask
from flask_restful import Api

from scikit_rest.resource import Prediction
from scikit_rest.validator import validate_type


def serve(col_list, col_types, transform_fn, predict_fn, port, is_nullable=False, name="model"):
    validate_type(col_types)
    app = Flask(name)
    api = Api(app)
    api.add_resource(
        Prediction,
        "/",
        resource_class_kwargs={
            "col_list": col_list,
            "col_types": col_types,
            "transform_fn": transform_fn,
            "predict_fn": predict_fn,
            "is_nullable": is_nullable,
        },
    )
    app.config["BUNDLE_ERRORS"] = True
    app.run(host="0.0.0.0", port=port)
