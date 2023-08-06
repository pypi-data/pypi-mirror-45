import datetime
import pandas as pd

from scikit_rest.type import is_date, is_bool, is_float, is_int, is_str


def validate_type(col_types):
    for key, items in col_types.items():
        assert items in [str, int, float, bool, datetime.datetime], (
            "Key {} has an unapproved type {}. Type must be one of the following : "
            "[str, int, float, bool, datetime.datetime ]".format(key, items)
        )


def validate_args(args, col_types, is_nullable):
    status_message = dict()
    for col, col_type in col_types.items():
        if col not in args.keys():
            status_message[col] = "input {} cannot be found in the payload".format(col)
        elif pd.isnull(args[col]):
            if (not is_nullable) or (col not in is_nullable):
                status_message[col] = "input {} is not supposed to be null".format(col)
        else:
            if col_type == datetime.datetime:
                if not is_date(args[col]):
                    status_message[col] = "input {} has wrong format (supposed to be {})".format(col, col_type)
            elif col_type == float:
                if not is_float(args[col]):
                    status_message[col] = "input {} has wrong format (supposed to be {})".format(col, col_type)
            elif col_type == int:
                if not is_int(args[col]):
                    status_message[col] = "input {} has wrong format (supposed to be {})".format(col, col_type)
            elif col_type == bool:
                if not is_bool(args[col]):
                    status_message[col] = "input {} has wrong format (supposed to be {})".format(col, col_type)
            else:
                if not is_str(args[col]):
                    status_message[col] = "input {} has wrong format (supposed to be {})".format(col, col_type)

    is_success = len(status_message) == 0
    return is_success, status_message
