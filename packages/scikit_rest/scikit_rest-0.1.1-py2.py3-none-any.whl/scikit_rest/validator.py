import datetime
import pandas as pd

from scikit_rest.types import validate_type

from typing import Dict, Union, List


def validate_col_types(col_types: Dict[str, Union[List, type]]):
    """assert that all the values within the dictionary is one of the following : [str, int, float, bool, datetime]"""
    for key, items in col_types.items():
        if isinstance(items, type):
            assert items in [str, int, float, bool, datetime.datetime], (
                "Key {} has an unapproved type {}. Type must be one of the following : "
                "[str, int, float, bool, datetime.datetime]".format(key, items)
            )
        else:
            assert isinstance(items, list), "values of key {} should be a list if it is not a type".format(key)
            for item in items:
                assert isinstance(item, str), "if col_types {} is a list, values must be type str".format(key)


def validate_args(
    args: Dict[str, Union[str, bool, int, float, datetime.datetime]],
    col_types: Dict[str, Union[List, type]],
    is_nullable: bool,
) -> [bool, Dict[str, str]]:
    """check whether the given arguments follows the specified types and follows the nullable rules"""
    status_message = dict()
    for col, col_type in col_types.items():
        if col not in args.keys():
            status_message[col] = "input {} cannot be found in the payload".format(col)
        elif pd.isnull(args[col]):
            if (not is_nullable) or (col not in is_nullable):
                status_message[col] = "input {} is not supposed to be null".format(col)
        else:
            if isinstance(col_type, list):
                if not validate_type(args[col], col_type):
                    status_message[col] = "input {} has to be one of the following {}".format(col, col_type)
            else:
                if not validate_type(args[col], col_type):
                    status_message[col] = "input {} has wrong format (supposed to be {})".format(col, col_type)
    is_success = len(status_message) == 0
    return is_success, status_message
