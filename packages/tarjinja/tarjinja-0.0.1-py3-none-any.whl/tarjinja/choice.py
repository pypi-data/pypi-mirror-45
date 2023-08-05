from .iface import Filter, Input, Output
from .jinjafilter import *
from .multifilter import *
from .reversefilter import *
from .strfilter import *

from .tar import *
from .zip import *
from .dirtree import *


def isX(v, x):
    if not isinstance(v, type):
        return False
    if not issubclass(v, x):
        return False
    if "Abstract" in v.__name__:
        return False
    if v is x:
        return False
    return True


def input_items():
    for k, v in globals().items():
        if isX(v, Input):
            if k.endswith("Input"):
                k = k[:-len("Input")]
            yield k, v


def output_items():
    for k, v in globals().items():
        if isX(v, Output):
            if k.endswith("Output"):
                k = k[:-len("Output")]
            yield k, v


def filter_items():
    for k, v in globals().items():
        if isX(v, Filter):
            if k.endswith("Filter"):
                k = k[:-len("Filter")]
            yield k, v
