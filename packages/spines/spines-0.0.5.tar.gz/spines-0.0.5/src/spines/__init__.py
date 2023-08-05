# -*- coding: utf-8 -*-
"""
Spines

Backbones for parameterized models.
"""
from .models import Model
from .parameters import Parameter, HyperParameter
from .parameters import Bounded, HyperBounded

__all__ = [
    # Models
    'Model',
    # Parameters
    'Parameter',
    'HyperParameter',
    'Bounded',
    'HyperBounded',
]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
