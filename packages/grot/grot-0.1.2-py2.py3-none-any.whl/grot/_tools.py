import itertools
import sys

import six

IS_PYTHON_2 = sys.version[0] == '2'

if IS_PYTHON_2:
    zip_ = itertools.izip
else:  # python3 and above
    zip_ = zip


def is_string(object_):
    return isinstance(object_, six.string_types)


def is_iterable(object_):
    try:
        from collections.abc import Iterable
    except ImportError:
        Iterable = tuple

    return isinstance(object_, Iterable)


def escape_string(string):
    if IS_PYTHON_2:
        return string.encode("string_escape")
    # in python3, 'string_escape' has become 'unicode_escape', but bytes is returned then,
    # that's why additional backward decode is needed
    return string.encode("unicode_escape").decode("utf-8")


def pairwise(iterable):
    if not iterable:
        return iterable
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip_(a, b)
