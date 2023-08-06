# -*- coding: utf-8 -*-
"""
Core configuration subpackage functionality.
"""
#
#   Imports
#
from typing import Dict
from typing import Type

from .base import BaseConfig


#
#   Configuration classes
#

class Config(BaseConfig):
    """
    Primary configuration class for spines.
    """
    __storage_cls__ = BaseConfig

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._plugins = {}
        return

    @property
    def plugins(self) -> Dict[str, Type['PluginConfig']]:
        """dict: Plugin configurations in this configuration."""
        return self._plugins

    def add_plugin(
        self, plugin: [str, Type['PluginConfig']], update: bool = False
    ) -> None:
        """Adds a plugin configuration to this config object

        Parameters
        ----------
        plugin : :obj:`str` or :obj:`PluginConfig`
            Plugin to add to this configuration.
        update : bool, optional
            Whether or not to update the existing plugin configuration
            with the new one or to replace it (default is :obj:`False`,
            replace).

        """
        from .utils import load_plugin_config

        if not isinstance(plugin, PluginConfig):
            plugin = load_plugin_config(plugin)
        p_name = plugin.name.lower()

        if update and p_name in self._plugins:
            self._plugins[p_name].update(plugin)
        else:
            self._plugins[p_name] = plugin
        return

    def remove_plugin(self, plugin: str) -> [Type['PluginConfig'], None]:
        """Removes a plugin configuration from this config object

        Parameters
        ----------
        plugin : str
            Name of the plugin to remove.

        Returns
        -------
        PluginConfig
            The plugin configuration removed from this configuration.

        """
        return self._plugins.pop(plugin.lower())


class PluginConfig(BaseConfig):
    """
    Plugin configuration class for spines.
    """
    __storage_cls__ = BaseConfig

    def __init__(self, name, *args, **kwargs):
        self._name = name
        return super().__init__(*args, **kwargs)

    @property
    def name(self) -> str:
        """str: Name of the plugin this configuration is for."""
        return self._name
