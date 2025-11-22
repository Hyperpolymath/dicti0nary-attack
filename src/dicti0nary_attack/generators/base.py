"""Base password generator class."""

from abc import ABC, abstractmethod
from typing import Iterator, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PasswordGenerator(ABC):
    """Abstract base class for password generators."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the password generator.

        Args:
            config: Configuration dictionary for the generator
        """
        self.config = config or {}
        self.stats = {
            "generated": 0,
            "filtered": 0,
        }

    @abstractmethod
    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate passwords.

        Args:
            count: Maximum number of passwords to generate (None for unlimited)

        Yields:
            Generated password strings
        """
        pass

    def apply_filters(self, password: str) -> bool:
        """
        Apply filters to determine if password should be included.

        Args:
            password: The password to filter

        Returns:
            True if password passes filters, False otherwise
        """
        min_length = self.config.get("min_length", 1)
        max_length = self.config.get("max_length", float("inf"))

        if len(password) < min_length or len(password) > max_length:
            self.stats["filtered"] += 1
            return False

        # Filter out actual dictionary words if configured
        if self.config.get("exclude_dictionary", False):
            # Placeholder for dictionary check
            pass

        return True

    def get_stats(self) -> Dict[str, int]:
        """Get generation statistics."""
        return self.stats.copy()

    def reset_stats(self):
        """Reset statistics counters."""
        self.stats = {
            "generated": 0,
            "filtered": 0,
        }
