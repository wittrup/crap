"""Function common
A collection of more or less well documented function for common usage

This should always be subject to
python -m pydoc -w FunCom
wrote FunCom.html
"""

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def avg(l):
    """:param l: list of numbers to be averaged
    :return:  average of numbers in list"""
    lg = len(l)
    if lg > 0:
        return sum(l) / lg
    else:
        return sum(l)

def dinc(dict, key, count=1):
    """dictionary increase, increases a key or creates if key does not exist
    :param dict:  target dictionary
    :param key:   key to increase
    :param count: size of increment"""
    dict[key] = count + dict[key] if key in dict else count

def even(number):
    """:param number: to be checked
    :return: Bool - True if number is even, False otherwise (return number % 2 == 0)"""
    return number % 2 == 0

def conv(value, fromLow=0, fromHigh=0, toLow=0, toHigh=0, func=None):
    """Re-maps a number from one range to another. That is, a value of fromLow would get mapped to toLow, a value of fromHigh to toHigh, values in-between to values in-between, etc.

Does not constrain values to within the range, because out-of-range values are sometimes intended and useful. The constrain() function may be used either before or after this function, if limits to the ranges are desired.

Note that the "lower bounds" of either range may be larger or smaller than the "upper bounds" so the conv() function may be used to reverse a range of numbers, for example
y = conv(x, 1, 50, 50, 1)

The function also handles negative numbers well, so that this example
y = conv(x, 1, 50, 50, -100)
is also valid and works well.

:param value:    the number to map
:param fromLow:  the lower bound of the value's current range
:param fromHigh: the upper bound of the value's current range
:param toLow:    the lower bound of the value's target range
:param toHigh:   the upper bound of the value's target range
:param func:     function to be applied on result
:return:         The mapped value."""
    result = (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
    if func is None:
        return result
    else:
        return func(result)