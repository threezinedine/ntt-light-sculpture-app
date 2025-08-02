from typing import Dict
import re


def get_raw_type_regex(type: str) -> str:
    """
    Getting the raw type (the primitive type) regex pattern.
    """
    return f"^[\\s\\S:]*{type}[\\s\\S]*$"


_RAW_TYPE_MAP: Dict[str, str] = {
    f"{get_raw_type_regex('int')}": "int",
    f"{get_raw_type_regex('float')}": "float",
    f"{get_raw_type_regex('double')}": "float",
    f"{get_raw_type_regex('bool')}": "bool",
    f"{get_raw_type_regex('string')}": "str",
}


def convert_type(type: str) -> str:
    """
    Convert the type from c++ header code into python type.
    """
    for regex, output in _RAW_TYPE_MAP.items():
        if re.match(regex, type):
            return output
    return None
