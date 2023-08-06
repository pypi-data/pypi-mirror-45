# -*- coding: utf-8 -*-
"""
Base classes for model parameters.
"""
#
#   Imports
#
from abc import ABC
from typing import Type


#
#   Base classes
#

class Parameter(object):
    """
    Parameter class

    Parameters
    ----------
    value_type : :obj:`type` or :obj:`Iterable` of :obj:`type`
        The type(s) of values allowed for this parameter.
    default : object, optional
        Default value for this parameter, if any.
    desc : str, optional
        Description for this parameter, if any.

    """

    def __init__(self, *value_type, default=None, desc: str = None):
        self._name = None
        self._desc = desc

        if not all([isinstance(x, type) for x in value_type]):
            raise TypeError('Must use types when setting this value')
        self._value_types = value_type

        if default is None:
            self._required = True
        else:
            if not isinstance(default, self.value_type):
                raise TypeError(
                    'Value type must be one of: %s' % self.value_type
                )
            self._required = False
        self._default = default
        return

    def __call__(self, value):
        try:
            if self._check_helper(value, raise_exceptions=True):
                return value
        except InvalidParameterException:
            value = self.preprocess(value)
            if not self._check_helper(value, raise_exceptions=False):
                raise
            return value
        return

    def __repr__(self) -> str:
        ret = '<%s %s [type=%s]' % (
                self.__class__.__name__,
                self.name,
                ', '.join([x.__name__ for x in self.value_type])
        )
        disp_props = self._disp_props()
        if disp_props:
            ret += " (%s)>" % ', '.join(self._disp_props())
        else:
            ret += ">"
        return ret

    def __str__(self) -> str:
        return self._name

    def __set_name__(self, owner, name: str) -> None:
        self._name = name
        return

    def __set__(self, instance: Type['spines.Model'], value) -> None:
        instance.parameters[self._name] = value
        return

    def __get__(self, instance, owner):
        return instance.parameters.get(self._name, None)

    @property
    def name(self) -> str:
        """str: Name of this parameter."""
        return self._name

    @property
    def desc(self) -> str:
        """str: Description of this parameter."""
        return self._desc

    @property
    def value_type(self) -> tuple:
        """tuple: The types of values allowed for this option."""
        return self._value_types

    @property
    def default(self):
        """object: Default value to use for this parameter."""
        return self._default

    @property
    def required(self) -> bool:
        """bool: Whether or not this parameter is required to be set."""
        return self._required

    def check(self, value) -> bool:
        """Checks the given `value` for validity

        Based on this particular Parameter's settings this method checks
        the given value to see if it's in-line with the specifications.

        Parameters
        ----------
        value
            Parameter value to check validity of.

        Returns
        -------
        bool
            Whether or not the value is valid for the parameter.

        See Also
        --------
        preprocess

        """
        return self._check_helper(value, raise_exceptions=False)

    def preprocess(self, value):
        """Pre-process/massage parameter values into correct type

        This is used to try and convert parameter values to the allowed
        types (if possible).  For instance the allowed type may be a
        :obj:`float` but the user provides ``1``, we would likely not
        want to break in that situation, but simply convert the
        :obj:`int` given into a :obj:`float`.  However, this can also be
        used to perform more complex initialization or customization on
        given parameter values, if needed.

        The default method is to try and cast the given value as the
        types given in this Parameter's ``_value_types`` attribute and
        returning the first successful cast, otherwise returns the given
        input `value`.

        This method can be easily extended or overridden for custom
        Parameter classes to handle more complex value types.

        Parameters
        ----------
        value : object
            The value to pre-process for this parameter.

        Returns
        -------
        object
            The pre-processed value.

        Note
        ----
        This method is, by default, only called if the given value fails
        this Parameter's ``check`` call.

        See Also
        --------
        check

        """
        for val_type in self._value_types:
            try:
                value = val_type(value)
                break
            except ValueError:
                pass
        return value

    def _check_helper(self, value, raise_exceptions=True) -> bool:
        """Helper function for checking if a value is valid"""
        if not isinstance(value, self.value_type):
            if raise_exceptions:
                raise InvalidParameterException(
                    '%s: invalid type given: %s (required %s)' % (
                        self.name, type(value),
                        ', '.join([str(x) for x in self.value_type])
                    )
                )
            return False

        return True

    def _disp_props(self):
        """Helper function to get properties to display in name string"""
        ret = list()
        if self.required:
            ret.append('required')
        if self.default:
            ret.append('default=%s' % self.default)
        return ret


class HyperParameter(Parameter):
    """
    Hyper-parameter
    """

    def __set__(self, instance: Type['spines.Model'], value) -> None:
        instance.hyper_parameters[self._name] = value
        return

    def __get__(self, instance: Type['spines.Model'], owner):
        return instance.hyper_parameters[self._name]


class ParameterMixin(ABC):
    """
    Base mixin class for parameters
    """

    def _check_helper(self, value, raise_exceptions: bool = True) -> bool:
        """Helper function to check if the given value is valid."""
        return super(ParameterMixin, self)._check_helper(
            value, raise_exceptions=raise_exceptions
        )


#
#   Exceptions
#

class ParameterException(Exception):
    """
    Base class for Model parameter exceptions.
    """
    pass


class MissingParameterException(ParameterException):
    """
    Thrown when a required parameter is missing.
    """
    pass


class InvalidParameterException(ParameterException):
    """
    Thrown when an invalid parameter is given.
    """
    pass
