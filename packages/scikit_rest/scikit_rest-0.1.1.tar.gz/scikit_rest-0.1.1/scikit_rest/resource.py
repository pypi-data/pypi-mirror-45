import numpy as np
import pandas as pd
from collections import OrderedDict
from flask_restful import Resource, reqparse
import sklearn

from scikit_rest.validator import validate_args
from scikit_rest.types import set_type

from typing import List, Dict, Union, Any, Callable


class Prediction(Resource):
    """class to handle ML prediction"""

    def __init__(self, **kwargs):
        self.col_list: List[str] = kwargs["col_list"]
        self.col_types: Dict[str, Union[List, type]] = kwargs["col_types"]
        self.transform_fn: Callable = kwargs["transform_fn"]
        self.predict_fn: Union[Callable, sklearn.base.BaseEstimator] = kwargs["predict_fn"]
        self.is_nullable: bool = kwargs["is_nullable"]

        self.parser: reqparse.RequestParser = reqparse.RequestParser()
        for col in self.col_list:
            self.parser.add_argument(col)
        self.args: Dict[str, Any] = self.parser.parse_args()

        self.result: Any = np.nan
        self.status_message: str = "Success"
        self.status_code: int = 200

        is_success, status_message = validate_args(self.args, self.col_types, self.is_nullable)
        if not is_success:
            self.status_message = status_message
            self.status_code = 400

    def output(self):
        return (
            {"data": {"result": self.result}, "message": {"status_message": self.status_message, "args": self.args}},
            self.status_code,
        )

    def get(self):
        if self.status_code == 200:
            input_dict = OrderedDict()
            for col in self.col_list:
                value = set_type(self.args[col], self.col_types[col])
                input_dict[col] = [value]
            input_df = pd.DataFrame(input_dict)
            transformed_df = self.transform_fn(input_df)
            if isinstance(self.predict_fn, sklearn.base.BaseEstimator):
                if hasattr(self.predict_fn, "predict_proba"):
                    if len(transformed_df) == 1:
                        self.result = self.predict_fn.predict_proba(transformed_df)[:, 1].item()
                    else:
                        self.result = self.predict_fn.predict_proba(transformed_df)[:, 1]
                elif hasattr(self.predict_fn, "predict"):
                    if len(transformed_df) == 1:
                        self.result = self.predict_fn.predict(transformed_df).item()
                    else:
                        self.result = self.predict_fn.predict(transformed_df)
                else:
                    self.status_code = 401
                    self.status_message = "predict_fn does not have attributes predict or predict_proba"
            else:
                self.result = self.predict_fn(transformed_df)
        return self.output()
