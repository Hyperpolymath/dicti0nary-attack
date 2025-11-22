"""Plugin system for dicti0nary-attack.

This module provides a simple plugin architecture for extending
the tool with custom generators, crackers, and other functionality.
"""

import importlib
import os
from typing import Dict, Any, Type, List
import logging

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages plugins for dicti0nary-attack."""

    def __init__(self):
        """Initialize the plugin manager."""
        self.generators: Dict[str, Type] = {}
        self.crackers: Dict[str, Type] = {}
        self.loaded_plugins: List[str] = []

    def register_generator(self, name: str, generator_class: Type):
        """
        Register a custom generator.

        Args:
            name: Name of the generator
            generator_class: Generator class to register
        """
        self.generators[name] = generator_class
        logger.info(f"Registered generator: {name}")

    def register_cracker(self, name: str, cracker_class: Type):
        """
        Register a custom cracker.

        Args:
            name: Name of the cracker
            cracker_class: Cracker class to register
        """
        self.crackers[name] = cracker_class
        logger.info(f"Registered cracker: {name}")

    def load_plugin(self, module_path: str):
        """
        Load a plugin from a module path.

        Args:
            module_path: Python module path (e.g., 'my_plugins.custom_gen')
        """
        try:
            module = importlib.import_module(module_path)

            # Look for register function
            if hasattr(module, 'register'):
                module.register(self)
                self.loaded_plugins.append(module_path)
                logger.info(f"Loaded plugin: {module_path}")
            else:
                logger.warning(f"Plugin {module_path} has no register() function")

        except ImportError as e:
            logger.error(f"Failed to load plugin {module_path}: {e}")
        except Exception as e:
            logger.error(f"Error loading plugin {module_path}: {e}")

    def load_plugins_from_directory(self, directory: str):
        """
        Load all plugins from a directory.

        Args:
            directory: Directory containing plugin modules
        """
        if not os.path.exists(directory):
            logger.warning(f"Plugin directory does not exist: {directory}")
            return

        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]
                module_path = f"{directory.replace('/', '.')}.{module_name}"
                self.load_plugin(module_path)

    def get_generator(self, name: str) -> Type:
        """
        Get a registered generator by name.

        Args:
            name: Name of the generator

        Returns:
            Generator class

        Raises:
            KeyError: If generator not found
        """
        if name not in self.generators:
            raise KeyError(f"Generator not found: {name}")
        return self.generators[name]

    def get_cracker(self, name: str) -> Type:
        """
        Get a registered cracker by name.

        Args:
            name: Name of the cracker

        Returns:
            Cracker class

        Raises:
            KeyError: If cracker not found
        """
        if name not in self.crackers:
            raise KeyError(f"Cracker not found: {name}")
        return self.crackers[name]

    def list_generators(self) -> List[str]:
        """Get list of registered generator names."""
        return list(self.generators.keys())

    def list_crackers(self) -> List[str]:
        """Get list of registered cracker names."""
        return list(self.crackers.keys())


# Global plugin manager instance
plugin_manager = PluginManager()


# Example plugin structure:
"""
# my_custom_plugin.py

from dicti0nary_attack.generators.base import PasswordGenerator
from typing import Iterator, Optional


class CustomGenerator(PasswordGenerator):
    '''My custom password generator.'''

    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        # Your implementation here
        yield "custom_password_1"
        yield "custom_password_2"


def register(plugin_manager):
    '''Register this plugin with the plugin manager.'''
    plugin_manager.register_generator('custom', CustomGenerator)
"""
