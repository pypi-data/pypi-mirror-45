# -*- coding: utf-8 -*-
"""
Primary configuration interface
"""
#
#   Imports
#
from typing import Tuple
from typing import Type

from . import utils
from .core import Config


#
#   Variables
#

_GLOBAL_CONFIG = None


#
#   Functions
#

def get_config() -> Type[Config]:
    """Get the global spines configuration

    Returns
    -------
    Config
        The global configuration settings for the current spines
        project.

    """
    if _GLOBAL_CONFIG is None:
        load_config()
    return _GLOBAL_CONFIG.copy()


def set_config(**settings) -> None:
    """Sets global configuration setting(s)

    Parameters
    ----------
    settings
        The setting(s) in the global configuration to update.

    """
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = _update_config(_GLOBAL_CONFIG, **settings)
    return


def load_config(*path: Tuple[str], update: bool = False) -> None:
    """Loads the global spines configuration

    Parameters
    ----------
    path : :obj:`str` (or multiple), optional
        File(s) to load the configuration from (defaults to the correct
        spines hierarchy for configuration files).
    update : bool, optional
        Update the current configuration as opposed to replacing it with
        the newly loaded on (default is :obj:`False`, replace it).

    """
    global _GLOBAL_CONFIG

    if not path:
        path = utils.find_config_files('.')

    if update:
        config = _GLOBAL_CONFIG
    else:
        config = None

    for p in path:
        config = _update_config(config, utils.load_config(p))

    _GLOBAL_CONFIG = config
    return


def _update_config(
    config: Type[Config], *other: Tuple[Type[Config]], **settings
) -> Type[Config]:
    """Updates the given configuration object"""
    if config is not None:
        updated = config.copy()
    else:
        updated = other[0]
        other = other[1:]

    for other_cfg in other:
        updated.update(other_cfg)

    if settings:
        updated.update(**settings)

    return updated
