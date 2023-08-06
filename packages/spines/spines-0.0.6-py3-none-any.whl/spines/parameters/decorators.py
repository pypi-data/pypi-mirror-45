# -*- coding: utf-8 -*-
"""
Decorators for parameters module.
"""
#
#   Imports
#
from functools import wraps
from typing import Type


#
#   Decorators
#

def state_changed(func):
    """Decorator indicating a function which changes the state

    Parameters
    ----------
    func : callable
        The function to wrap.

    Returns
    -------
    callable
        The wrapped function.

    """
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        self._finalized = False
        return ret
    return wrapped


def finalize_pre(func, store: Type['ParameterStore']):
    """Finalizes the store prior to executing the function

    Parameters
    ----------
    func : callable
        The function to wrap.
    store : ParameterStore
        The parameter store to finalize.

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


def finalize_post(func, store: Type['ParameterStore']):
    """Finalizes the store prior to executing the function

    Parameters
    ----------
    func : callable
        The function to wrap.
    store : ParameterStore
        The parameter store to finalize.

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
