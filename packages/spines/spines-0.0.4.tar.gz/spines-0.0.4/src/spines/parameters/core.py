# -*- coding: utf-8 -*-
"""
Parameter classes for use in models.
"""
#
#   Imports
#
from .base import Parameter
from .base import HyperParameter
from . import mixins


#
#   Parameter classes
#

class Bounded(mixins.Minimum, mixins.Maximum, Parameter):
    """
    Bounded parameter (min/max)
    """
    pass


class HyperBounded(mixins.Minimum, mixins.Maximum, HyperParameter):
    """
    Bounded hyper-parameter (min/max)
    """
    pass
