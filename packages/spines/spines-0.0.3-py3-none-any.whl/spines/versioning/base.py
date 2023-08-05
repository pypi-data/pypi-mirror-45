# -*- coding: utf-8 -*-
"""
Base classes for the spines versioning package.
"""
#
#   Imports
#
import parver

from .core import slugify


#
#   Classes
#

class Version(object):
    """
    Version objects for versioning of spines components
    """

    def __init__(self, name, display_name=None, desc=None):
        self._name = name
        self._display_name = display_name
        self._desc = desc
        self._version = parver.Version((0, 0, 1), dev=None)
        self._tag = None

    # dunder methods

    def __repr__(self):
        return "<Version name=%s version=%s>" % (self._name, self._version)

    def __str__(self):
        return '%s %s' % (self._name, self._version)

    # Properties

    @property
    def name(self) -> str:
        """str: Name of the object versioned."""
        return self._name

    @property
    def display_name(self) -> str:
        """str: Display name for the object versioned."""
        return self._display_name

    @display_name.setter
    def display_name(self, value) -> None:
        self._display_name = value
        return

    @property
    def description(self) -> str:
        """str: Description for the object versioned."""
        return self._desc

    @description.setter
    def description(self, value) -> None:
        self._desc = value
        return

    @property
    def tag(self) -> str:
        """str: Tag (if any) for this version."""
        return self._tag

    @tag.setter
    def tag(self, value) -> None:
        self._tag = value
        return

    @property
    def version(self) -> str:
        """str: Version string for this version object."""
        return str(self._version)

    @property
    def slug(self) -> str:
        """str: Slugified version of this version object"""
        slug_name = slugify(self._name)
        slug_vers = slugify(str(self._version))
        return '%s/%s' % (slug_name, slug_vers)

    # Version actions

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

    def bump_dev(self) -> None:
        """Bumps the dev number for use during iterative work."""
        self._version = self._version.bump_dev()
        return

    def bump(self) -> None:
        """Bumps this version's PATCH number by one."""
        self._version = self._version.bump_release(index=2)
        return

    def bump_minor(self) -> None:
        """Bumps this version's MINOR number by one."""
        self._version = self._version.bump_release(index=1)
        return

    def bump_major(self) -> None:
        """Bumps this version's MAJOR number by one."""
        self._version = self._version.bump_release(index=0)
        return


class Signature(object):
    """
    Signature objects for component change tracking and management
    """
    pass
