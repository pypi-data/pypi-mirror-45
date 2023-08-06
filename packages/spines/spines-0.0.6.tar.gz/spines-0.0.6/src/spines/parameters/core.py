# -*- coding: utf-8 -*-
"""
Parameter classes for use in models.
"""
#
#   Imports
#
from . import mixins
from .base import Parameter
from .base import HyperParameter


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
