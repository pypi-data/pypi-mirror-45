# -*- coding: utf-8 -*-
"""
Decorators for Models
"""
#
#   Imports
#
from functools import wraps
from typing import Type

from ..parameters.store import ParameterStore


#
#   Decorators
#

def finalize_pre(store: Type[ParameterStore], func):
    """Finalizes the store prior to executing the function

    Parameters
    ----------
    store : ParameterStore
        The parameter store to finalize.
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The wrapped function.

    Raises
    ------
    MissingParameterException
        If there's a parameter missing from the required parameters in
        the given `store`.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not store.final:
            store.finalize()
        return func(*args, **kwargs)
    return wrapper


def finalize_post(store: Type[ParameterStore], func):
    """Finalizes the store prior to executing the function

    Parameters
    ----------
    store : ParameterStore
        The parameter store to finalize.
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The wrapped function.

    Raises
    ------
    MissingParameterException
        If there's a parameter missing from the required parameters in
        the given `store`.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if not store.final:
            store.finalize()
        return ret
    return wrapper
