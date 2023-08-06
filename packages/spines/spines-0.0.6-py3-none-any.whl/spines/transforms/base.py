# -*- coding: utf-8 -*-
"""
Base classes for transforms subpackage.
"""
#
#   Imports
#
from abc import ABCMeta
from abc import abstractmethod
from typing import Dict

from ..core.base import BaseObject


#
#   Base class
#

class Transform(BaseObject, metaclass=ABCMeta):
    """
    Base Transform class
    """

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.transform(*args, **kwargs)

    def construct(self, *args, **kwargs) -> None:
        """Constructs the transformer prior to use

        Parameters
        ----------
        args : optional
            Arguments to use in constructing the transformer.
        kwargs : optional
            Keyword arguments to use in constructing the transformer.

        """
        return

    def fit(self, *args, **kwargs) -> [Dict[str, object], None]:
        """Fits the parameters for this transformation

        Parameters
        ----------
        args
            Data to use for fitting this Transformer.
        kwargs : optional
            Additional keyword-arguments to use in fit call.

        Returns
        -------
        :obj:`dict` or :obj:`None`
            Dictionary of updates from fit, or :obj:`None`.

        """
        return

    def score(self, *args, **kwargs) -> float:
        """Returns the score measure for this Transform

        Parameters
        ----------
        args : optional
            Arguments (data inputs and outputs) to pass to the score
            call.
        kwargs : optional
            Additional keyword-arguements to pass to the score call.

        Returns
        -------
        float
            Score for the given inputs and outputs.

        """
        return

    @abstractmethod
    def transform(self, *args, **kwargs):
        """Transforms the given data

        Parameters
        ----------
        args
            Data to perform transformation on.
        kwargs : optional
            Additional keyword arguments to use in transform call.

        Returns
        -------
        object
            Transformed inputs.

        """
        pass
