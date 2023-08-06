from typing import Optional
import math

def parse_int(s: str) -> Optional[int]:
    """
    return s as an integer, if possible; returns None if s is not an integer
    
    For example, parse_int('3') returns 3, but parse_int('3.2') and 
    parse_int('argh') both return None.
    """
    
    if type(s) is not int and type(s) is not str:
        return None
    try:
        return int(s)
    except ValueError:
        return None

def parse_float(s: str) -> Optional[float]:
    """
    return s as a float, if possible; returns None if s is not a float
    
    For example, parse_float('3') returns 3.0 and parse_float('3.2') returns 3.2, 
    but parse_float('argh') returns None.
    
    NOTE: parse_float('NaN') returns None, even though technically NaN is a 
    special float value meaning 'not a number'.
    """

    if type(s) is not float and type(s) is not str:
        return None
    try:
        f = float(s)
        if math.isnan(f):
            return None
        else:
            return f
    except ValueError:
        return None

def parse_bool(s: str) -> Optional[bool]:
    if type(s) is not bool and type(s) is not str:
        return None
    if len(s) == 0:
        return None
    if s == "0" or s.lower() == "false":
        return False
    return True

# be aware that the overall cs103 library has its own __all__
__all__ = ['parse_int', 'parse_float']  # parse_bool is NOT presently exported