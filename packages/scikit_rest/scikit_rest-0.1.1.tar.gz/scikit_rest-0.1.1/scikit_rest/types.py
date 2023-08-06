import datetime
from dateutil.parser import parse
from typing import Union, Any
import numpy

true_list = ["True", "true", "T", "t", "1"]
false_list = ["False", "false", "F", "f", "0"]
numpy_dict = {
    numpy.int64: int,
    numpy.float64: float,
    numpy.bool_: bool,
    numpy.object_: str,
    numpy.str_: str,
    numpy.datetime64: datetime.datetime,
}


def is_int(value: Union[str, float, int]) -> bool:
    """validate whether the value is integer"""
    try:
        value = float(value)
        return value.is_integer()
    except ValueError:
        return False


def is_date(value: Union[str, datetime.datetime]) -> bool:
    """validate whether the value is datetime"""
    try:
        parse(str(value), fuzzy=False)
        return True
    except ValueError:
        return False


def is_float(value: Union[str, float]) -> bool:
    """validate whether the value is float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_str(value: Union[str]) -> bool:
    """validate whether the value is string"""
    return isinstance(value, str)


def is_bool(value: Union[str, bool]) -> bool:
    """validate whether the value is boolean"""
    return (value in true_list + false_list) or (isinstance(value, bool))


def validate_type(value: Union[int, float, bool, str, datetime.datetime], value_type: Union[type]) -> bool:
    """ Validate the type of the value"""

    if value_type == int:
        result = is_int(value)
    elif value_type == float:
        result = is_float(value)
    elif value_type == bool:
        result = is_bool(value)
    elif value_type == datetime.datetime:
        result = is_date(value)
    elif value_type == str:
        result = is_str(value)
    elif isinstance(value_type, list):
        result = str(value) in value_type
    else:
        raise ValueError("data type not recognized : {}".format(value))
    return result


def set_type(value: Union[str, bool, int, float, datetime.datetime], value_type: Union[type, list]) -> Any:
    """Convert the value to be the appropriate type, based on the given value_type"""
    if value_type == int:
        value = int(value)
    elif value_type == float:
        value = float(value)
    elif value_type == bool:
        value = value in true_list
    elif value_type == datetime.datetime:
        value = parse(value)
    elif value_type == str:
        value = str(value)
    elif isinstance(value_type, list):
        value = str(value)
    else:
        raise ValueError("data type not recognized : {}".format(value))
    return value
