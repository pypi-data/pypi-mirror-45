# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning functionality.
"""
#
#   Imports
#
from abc import ABC
from abc import abstractmethod
from hashlib import blake2s
from typing import Dict
from typing import Tuple
from typing import Type

import parver
from xxhash import xxh64

from .. import __version__
from ..parameters.base import Parameter
from .utils import slugify


#
#   Classes
#

class BaseSignature(ABC):
    """
    Base signature objects for component change tracking and management.

    This object is used for tagging/version-tracking a single component
    of a larger model (e.g. the ``fit`` method).  Collections of these
    objects are used to identify, fully, a particular version of a
    :class:`Model` instance.

    """
    _HASH = xxh64

    def __init__(self, obj):
        if not isinstance(obj, type):
            obj = obj.__class__
        self._name = obj.__name__
        self._hash = self._get_hash(obj).digest()

    def __str__(self):
        return '%s @ %s' % (self.name, self.hash[-8:])

    def __repr__(self):
        return '<Signature: name="%s" hash="%s">' % (
            self.name, self.hash[-8:]
        )

    @property
    def hash(self) -> str:
        """str: Full hash string for this signature's hash"""
        return self._hash.hex()

    @property
    def hash_bytes(self) -> bytes:
        """bytes: Full hash (in bytes-form) for this signature"""
        return self._hash

    @property
    def name(self) -> str:
        """str: The name of the object this signature is for"""
        return self._name

    @classmethod
    def _get_hash(cls, obj) -> [bytes, None]:
        """Gets the hash for the given object"""
        m = cls._HASH()
        m.update(cls._get_bytes(obj))
        return m

    @abstractmethod
    @classmethod
    def _get_bytes(cls, obj) -> bytes:
        """Gets the relevant bytes for a single object"""
        pass


class BaseVersion(BaseSignature):
    """
    Base version object for versioning module.

    Parameters
    ----------
    obj : object
        The object to generate a version object for.

    """
    _HASH = blake2s

    def __init__(self, obj):
        if not isinstance(obj, type):
            obj = obj.__class__
        self._spines_version = __version__
        self._desc = self._get_desc(obj)

        super(BaseVersion, self).__init__(obj)

        self._version = self._determine_next_version(
            obj.__getattribute__('__version__', None)
        )

    def __repr__(self):
        return '<Version: name="%s" version="%s">' % (
            self.name, self.version
        )

    @property
    def name(self) -> str:
        """str: Name of the object versioned."""
        return self._name

    @property
    def description(self) -> str:
        """str: Docstring for the main object versioned."""
        return self._desc

    @property
    def slug(self) -> str:
        """str: Slugified version of this version object"""
        slug_name = slugify(self._name)
        slug_vers = slugify(str(self._version))
        return '%s/%s' % (slug_name, slug_vers)

    @property
    def spines_version(self) -> str:
        """str: Version of spines this version object was created with
        """
        return self._spines_version

    @property
    def version(self) -> str:
        """str: Version string for this version object."""
        return str(self._version)

    # Version switches

    def to_release(self) -> None:
        """Switches the version to release"""
        self._version = self._version.clear(dev=False, pre=False, post=False)
        return

    def to_pre(self) -> None:
        """Switches the version to pre-release"""
        self._version = self._version.clear(pre=True)
        return

    def to_post(self) -> None:
        """Switches the version to post-release"""
        self._version = self._version.clear(post=True)
        return

    def to_dev(self) -> None:
        """Switches the version to development"""
        self._version = self._version.clear(dev=True)
        return

    # Versioning logic

    def _get_next_version(
        self,
        prev_version: [Type['Version'], None]
    ) -> Type[parver.Version]:
        """Determines the next version from the previous"""
        if prev_version is None:
            return parver.Version((0, 0, 1), dev=None)
        return

    # Helper methods

    @classmethod
    def _get_desc(cls, obj) -> [str, None]:
        """Helper function to get description of this versioned object
        """
        return getattr(obj, '__doc__', None)

    @classmethod
    def _get_signatures_helper(
        cls, obj, signature_cls: type, *allowed_types: Tuple[type]
    ) -> Tuple[Dict[str, Type[Parameter]], Dict[str, Type['Signature']]]:
        """Helper function to get individual model parameters"""
        if not allowed_types:
            allowed_types = object
        ret, sigs = {}, {}
        for k, v in obj.__dict__.items():
            if isinstance(v, allowed_types):
                ret[k] = v
                sigs[k] = signature_cls(v)
        return ret, sigs
