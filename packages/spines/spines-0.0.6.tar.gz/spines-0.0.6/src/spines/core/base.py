# -*- coding: utf-8 -*-
"""
Base classes for core spines library.
"""
#
#   Imports
#
from abc import ABC
import tempfile
from typing import List
from typing import Type

from ..parameters.base import Parameter
from ..parameters.store import ParameterStore
from ..utils.file import extract_archive
from ..utils.file import save_archive
from ..utils.file import save_pickle
from ..utils.file import load_pickle
from .decorators import override
from .utils import get_overridden_methods


#
#   Classes
#

class BaseObject(ABC):
    """
    Base object class for all spines components
    """
    __version__ = None
    __param_store__ = ParameterStore

    def __init__(self, *args, **kwargs):
        self._params = self._create_store(
            self.__param_store__, Parameter
        )
        self._modify_methods()
        return

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '<%s version="%s" parameters="%s">' % (
            self.__class__.__name__, self.__version__,
            ', '.join(sorted(self.parameters.keys()))
        )

    @property
    def parameters(self) -> Type[ParameterStore]:
        """ParameterStore: Parameters in this object."""
        return self._params

    def set_params(self, **params) -> None:
        """Sets the values for this model's parameters

        Parameters
        ----------
        params
            Parameters and values to set.

        Raises
        ------
        InvalidParameterException
            If the given `name` or `value` are not valid.

        """
        self._params.update(params)
        return

    def get_params(self) -> dict:
        """Gets a copy of this models parameters

        Returns
        -------
        dict
            Copy of currently set parameter names and values.

        """
        return self._params.values

    def set_parameter(self, name: str, value) -> None:
        """Sets a parameter value

        Will add the given `param` and `value` to the parameters if
        they are valid, throws an exception if they are not.

        Parameters
        ----------
        name : str
            Parameter to set the value for.
        value
            Value to set.

        Raises
        ------
        InvalidParameterException
            If the given `name` or `value` are not valid.

        See Also
        --------
        parameters

        """
        self._params[name] = value
        return

    def unset_parameter(self, name: str) -> object:
        """Unsets a parameter value

        Removes the specified parameter's value from the parameter
        values if it is part of the parameter set and returns its
        current value.

        Parameters
        ----------
        name : str
            Name of the parameter whose value needs to be un-set.

        Returns
        -------
        object
            Previously set value of the parameter.

        Raises
        ------
        MissingParameterException
            If the parameter to remove does not exist in the set of
            parameters.

        See Also
        --------
        parameters

        """
        return self._params.pop(name)

    def save(
        self, path: [None, str] = None, fmt: [None, str] = None
    ) -> str:
        """Saves this object to file

        Parameters
        ----------
        path : str, optional
            File path to save this object to.
        fmt : str, optional
            Format to save this object with.

        Returns
        -------
        str
            Path to the saved object file.

        """
        if path is None:
            self._get_file_path()

        with tempfile.TemporaryDirectory(prefix='spines-') as tmp_dir:
            files = self._save_helper(tmp_dir)
            return save_archive(path, files, fmt=fmt)

    def _save_helper(self, dir_path: str) -> List[str]:
        """Saves the relevant parts of this object to file

        Parameters
        ----------
        dir_path : str
            Path to the directory to save the files to.

        Returns
        -------
        :obj:`list` of :obj:`str`
            List of files saved.

        """
        ret = list()
        ret.append(save_pickle(self.__class__, dir_path, 'class'))
        ret.append(save_pickle(self._params, dir_path, 'parameters'))
        return ret

    @classmethod
    def load(
        cls, path: str, fmt: [None, str] = None, new: bool = False
    ) -> Type['BaseObject']:
        """Loads an object from file

        Parameters
        ----------
        path : str
            Path to the file to load from.
        fmt : str, optional
            Format to use when loading the file (default is :obj:`None`
            which will infer based on the `path`, if possible).
        new : bool, optional
            Whether or not to create a new instance from this (the
            calling) class or to use the stored class object (default is
            :obj:`False`, use the saved version).

        Returns
        -------
        BaseObject
            The new object loaded from file.

        """
        with tempfile.TemporaryDirectory(prefix='spines-') as tmp_dir:
            extract_archive(path, tmp_dir, fmt=fmt)
            return cls._load_helper(tmp_dir, new)

    @classmethod
    def _load_helper(cls, dir_path: str, new: bool) -> Type['BaseObject']:
        """Loads the various files into a new object"""
        if new:
            instance = cls()
        else:
            instance = load_pickle(dir_path, 'class')()
        instance._params = load_pickle(dir_path, 'parameters')
        return instance

    def _get_file_path(self) -> str:
        """Gets the default file path for saving to"""
        pass

    def _modify_methods(self, *args, **kwargs) -> None:
        """Helper function to modify this classes methods"""
        self._mark_overridden_methods()
        return

    @classmethod
    def _create_store(cls, store_cls, param_cls) -> Type[ParameterStore]:
        """Creates and instance of the parameter store"""
        store = store_cls()
        for attr in cls.__dict__.values():
            if isinstance(attr, param_cls):
                store.add(attr)
        return store

    def _mark_overridden_methods(self) -> None:
        """Marks the methods overridden in this object's implementation
        """
        base_cls = type(self).__bases__[-1]
        for method in get_overridden_methods(base_cls, self):
            setattr(self, method, override(getattr(self, method)))
        return


#
#   Exceptions
#

class BaseObjectException(Exception):
    """
    Base exception class for spines objects.
    """
    pass
