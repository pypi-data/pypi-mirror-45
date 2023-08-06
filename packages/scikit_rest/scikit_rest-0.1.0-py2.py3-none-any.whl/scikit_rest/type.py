import datetime
from dateutil.parser import parse

true_list = ["True", "true", "T", "t", "1"]
false_list = ["False", "false", "F", "f", "0"]


def is_int(value):
    try:
        value = float(value)
        return value.is_integer()
    except ValueError:
        return False


def is_date(string):
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_str(value):
    return isinstance(value, str)


def is_bool(value):
    return value in true_list + false_list


def set_type(value, type):
    if type == datetime.datetime:
        value = parse(value)
    elif type == int:
        value = int(value)
    elif type == float:
        value = float(value)
    elif type == bool:
        value = value in true_list
    else:
        value = str(value)
    return value
