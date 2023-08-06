# -*- coding: utf-8 -*-
"""
Utilities for the spines core classes.
"""
#
#   Imports
#
from typing import Type


#
#   Functions
#

def get_overridden_methods(cls: type, obj: Type['spines.base.BaseObject']):
    """Get the overridden methods in an object.

    Parameters
    ----------
    cls : type
        Base class to compare against.
    obj : BaseObject
        Object instance to get methods which are overridden.

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of the methods which are overridden in the `obj`.

    """
    common = cls.__dict__.keys() & obj.__class__.__dict__.keys()
    return [
        m for m in common if cls.__dict__[m] != obj.__class__.__dict__[m]
        and callable(cls.__dict__[m])
    ]
