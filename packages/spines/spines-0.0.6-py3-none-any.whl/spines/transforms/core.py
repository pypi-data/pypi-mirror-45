# -*- coding: utf-8 -*-
"""
Core Transform classes for manipulating data.
"""
#
#   Imports
#
from ..parameters.base import Parameter
from .base import Transform


#
#   Transform classes
#

class Pass(Transform):
    """
    Transform which simply passes the given values through
    """
    output = Parameter(type, default=None)

    def transform(self, *args, **kwargs):
        """Passes the given input `args` back out

        If this transform's `output` parameter is set, it will attempt
        to call it's :obj:`__call__` with the given `args` and `kwargs`.
        If no `output` parameter is set this will return the input
        `args` as a :obj:`tuple` if they have a length greater than one
        otherwise it will just return the first input element of `args`.

        Parameters
        ----------
        args
            Input data to pass back out.
        kwargs : optional
            Additional keyword arguments to use if `output` parameter
            is set.

        """
        if self.output is None:
            if len(args) == 1:
                return args[0]
            return args
        return self.output(*args, **kwargs)
