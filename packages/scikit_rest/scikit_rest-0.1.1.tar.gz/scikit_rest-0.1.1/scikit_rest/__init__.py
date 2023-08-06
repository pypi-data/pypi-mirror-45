"""Automatically serve ML model as a REST API"""
__version__ = "0.1.1"

from typing import List, Dict, Union, Callable

import pandas as pd
import sklearn
from flask import Flask
from flask_restful import Api

from scikit_rest.resource import Prediction
from scikit_rest.types import numpy_dict
from scikit_rest.validator import validate_col_types


def infer(input_df: pd.DataFrame) -> [List[str], Dict[str, Union[List, type]]]:
    """
    Automatically infer the column list and column types from the input DataFrame

    Args:
        input_df: DataFrame, where the column list and column types will be inferred from.

    Returns:
        col_list: List of Column names, where the order of the values will dictate the order within the pandas DataFrame
        col_types: Dictionary of Column Names and the type of the variable, used for input Validation. If the values
        of the dictionary is instead a list, We assume that any input for the variable can only be any of
         the ones listed within the list
    """
    df = input_df.copy().infer_objects()
    col_list = df.columns.tolist()
    col_types = {}
    for key, value in df.dtypes.to_dict().items():
        col_types[key] = numpy_dict[value.type]
    return col_list, col_types


def serve(
    col_list: List[str],
    col_types: Dict[str, Union[List, type]],
    transform_fn: Callable,
    predict_fn: Union[Callable, sklearn.base.BaseEstimator],
    port: int = 1234,
    is_nullable: bool = False,
    name: str = "model",
):
    """
    Setting up ML model as a REST API server

    Args:
        col_list: List of Column names, where the order of the values will dictate the order within the pandas DataFrame
        col_types: Dictionary of Column Names and the type of the variable, used for input Validation. If the values
        of the dictionary is instead a list, We assume that any input for the variable can only be any of
         the ones listed within the list
        transform_fn: Function which convert the input dataframe into test dataframe,
        where we can call model.predict upon to get the final result
        predict_fn: Function which convert the test dataframe into result. If a ML model instance is passed in, we will
        instead try to call model.predict_proba / model.predict to get the result
        port: Port Number where the REST API should be served upon
        is_nullable: Whether input API can be nullable
        name: Name of the program
    """
    validate_col_types(col_types)
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
