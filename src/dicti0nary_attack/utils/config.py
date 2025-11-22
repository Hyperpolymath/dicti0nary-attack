"""Configuration management."""

import os
import yaml
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages configuration loading and validation."""

    DEFAULT_CONFIG = {
        'generators': {
            'leetspeak': {
                'max_substitutions': 3,
                'min_length': 6,
                'max_length': 16,
            },
            'phonetic': {
                'case_variations': True,
                'min_length': 4,
                'max_length': 20,
            },
            'pattern': {
                'min_length': 6,
                'max_length': 16,
            },
            'random': {
                'min_length': 8,
                'max_length': 16,
                'use_uppercase': True,
                'use_lowercase': True,
                'use_digits': True,
                'use_special': False,
            },
            'markov': {
                'order': 2,
                'min_length': 6,
                'max_length': 16,
            },
        },
        'cracker': {
            'algorithm': 'sha256',
            'workers': 4,
            'batch_size': 1000,
        },
        'output': {
            'format': 'text',
            'directory': 'output',
            'save_stats': True,
        },
        'logging': {
            'level': 'INFO',
            'file': None,
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to configuration file (YAML or JSON)
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()

        if config_path:
            self.load_config(config_path)

    def load_config(self, filepath: str):
        """
        Load configuration from file.

        Args:
            filepath: Path to config file
        """
        try:
            with open(filepath, 'r') as f:
                if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    loaded_config = yaml.safe_load(f)
                elif filepath.endswith('.json'):
                    loaded_config = json.load(f)
                else:
                    logger.error(f"Unsupported config format: {filepath}")
                    return

                if loaded_config:
                    self._merge_config(self.config, loaded_config)
                    logger.info(f"Loaded configuration from {filepath}")

        except FileNotFoundError:
            logger.warning(f"Config file not found: {filepath}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")

    def _merge_config(self, base: Dict, updates: Dict):
        """
        Recursively merge configuration dictionaries.

        Args:
            base: Base configuration dictionary
            updates: Updates to merge in
        """
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path (e.g., 'cracker.algorithm')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.

        Args:
            key_path: Dot-separated path (e.g., 'cracker.algorithm')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def save_config(self, filepath: str):
        """
        Save current configuration to file.

        Args:
            filepath: Path to output file
        """
        try:
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)

            with open(filepath, 'w') as f:
                if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False, indent=2)
                elif filepath.endswith('.json'):
                    json.dump(self.config, f, indent=2)
                else:
                    logger.error(f"Unsupported config format: {filepath}")
                    return

            logger.info(f"Saved configuration to {filepath}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def get_generator_config(self, generator_type: str) -> Dict[str, Any]:
        """
        Get configuration for a specific generator.

        Args:
            generator_type: Type of generator

        Returns:
            Generator configuration dictionary
        """
        return self.config.get('generators', {}).get(generator_type, {})

    def get_cracker_config(self) -> Dict[str, Any]:
        """Get cracker configuration."""
        return self.config.get('cracker', {})

    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self.config.get('output', {})
