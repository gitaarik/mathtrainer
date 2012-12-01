"""
Validate a variable.

This module provides several validation functions.
They return True if the validation succeeds, otherwise they return False.

"""

def floatnum(var):
    """
    Validate a floating point number.
    """
    try:
        float(var)
        return True
    except ValueError:
        return False
