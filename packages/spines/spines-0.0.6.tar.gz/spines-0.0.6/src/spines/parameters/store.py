# -*- coding: utf-8 -*-
"""
Parameter storage module.
"""
#
#   Imports
#
from collections.abc import MutableMapping
from typing import Dict
from typing import Iterator
from typing import Type

from .base import Parameter
from .base import MissingParameterException
from .decorators import state_changed


#
#   Classes
#

class ParameterStore(MutableMapping):
    """
    Helper class for managing collections of Parameters.
    """

    def __init__(self):
        self._params = dict()
        self._values = dict()
        self._finalized = True
        return

    def __repr__(self):
        ret = "<%s final=%s> {\n" % (self.__class__.__name__, self._finalized)
        for k, v in self._params.items():
            ret += "  %s: %s,\n" % (repr(v), self._values.get(k))
        ret += "}"
        return ret

    def __str__(self):
        ret = "{\n"
        for k, v in self._params.items():
            ret += "  %s: %s\n" % (v, self._values.get(k))
        ret += "}"
        return ret

    @state_changed
    def __setitem__(self, k: str, v) -> None:
        self._values[k] = self._params[k](v)
        return

    @state_changed
    def __delitem__(self, v: str) -> None:
        del self._values[v]

    def __getitem__(self, k: str):
        return self._values[k]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    @property
    def parameters(self) -> Dict[str, Parameter]:
        """dict: Copy of the current set of parameters."""
        return self._params.copy()

    @property
    def values(self) -> Dict[str, object]:
        """dict: Copy of the current set of parameter values."""
        return self._values.copy()

    @property
    def valid(self) -> bool:
        """bool: Whether or not this is a fully valid set of parameters."""
        return self._validate_helper(raise_exceptions=False)

    @property
    def final(self) -> bool:
        """bool: Whethor or not this set of parameters is finalized."""
        return self._finalized

    def copy(self, deep: bool = False) -> Type['ParameterStore']:
        """Returns a copy of this parameter store object.

        Parameters
        ----------
        deep : bool, optional
            Whether or not to do deep-copying of this stores contents.

        Returns
        -------
        ParameterStore
            Copied parameter store object.

        """
        new_obj = self.__class__()
        for k, v in self._params:
            new_obj.add(v)
        for k, v in self._values:
            new_obj[k] = v
        if self._finalized:
            new_obj.finalize()
        return new_obj

    @state_changed
    def reset(self) -> None:
        """Clears all of the parameters and options stored."""
        self._values.clear()
        self._params.clear()

    @state_changed
    def add(self, parameter: Type[Parameter]) -> None:
        """Add a :class:`Parameter` specification to this store

        Parameters
        ----------
        parameter : Parameter
            :class:`Parameter` specification to add to this parameter
            store.

        Raises
        ------
        ParameterExistsError
            If a parameter option with the same name already exists.

        """
        self._params[parameter.name] = parameter
        return

    @state_changed
    def remove(self, name: str) -> Parameter:
        """Removes a :class:`Parameter` specification

        Parameters
        ----------
        name : str
            Name of the :class:`Parameter` to remove.

        Returns
        -------
        Parameter
            The removed :class:`Parameter` specified.

        Raises
        ------
        KeyError
            If the given `name` does not exist.

        """
        if name in self._values.keys():
            del self._values[name]
        return self._params.pop(name)

    def finalize(self) -> None:
        """Finalizes the parameters stored

        Raises
        ------
        MissingParameterException
            If a required parameter is not set.

        """
        if self._validate_helper(raise_exceptions=True):
            for k, v in self._params.items():
                if k not in self._values.keys():
                    self._values[k] = v.default
            self._finalized = True
        return

    def _validate_helper(self, raise_exceptions: bool = False) -> bool:
        """Helper to check if this set of parameters is valid"""
        for k, v in self._params.items():
            if v.required and k not in self._values.keys():
                if raise_exceptions:
                    raise MissingParameterException(k)
                return False
        return True
