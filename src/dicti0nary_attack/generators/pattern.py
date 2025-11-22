"""Pattern-based password generator."""

import itertools
import string
from typing import Iterator, Optional, Dict, Any, List
from dicti0nary_attack.generators.base import PasswordGenerator


class PatternGenerator(PasswordGenerator):
    """
    Generates passwords based on common patterns.

    Targets predictable patterns like "abc123", "qwerty123",
    keyboard walks, repeating patterns, etc.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the pattern generator.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.min_length = self.config.get("min_length", 6)
        self.max_length = self.config.get("max_length", 16)

    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate pattern-based passwords.

        Args:
            count: Maximum number of passwords to generate

        Yields:
            Pattern-based passwords
        """
        generated = 0
        generators = [
            self._keyboard_walks(),
            self._repeating_patterns(),
            self._sequential_patterns(),
            self._date_patterns(),
            self._number_suffix_patterns(),
        ]

        for gen in generators:
            for password in gen:
                if count and generated >= count:
                    return

                if self.apply_filters(password):
                    self.stats["generated"] += 1
                    generated += 1
                    yield password

    def _keyboard_walks(self) -> Iterator[str]:
        """Generate keyboard walk patterns."""
        # QWERTY keyboard rows
        rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm",
            "1234567890",
        ]

        # Generate walks of different lengths
        for row in rows:
            for length in range(self.min_length, min(len(row) + 1, self.max_length + 1)):
                for start in range(len(row) - length + 1):
                    walk = row[start:start + length]
                    yield walk
                    yield walk.upper()
                    yield walk.capitalize()

                    # Add reverse walks
                    yield walk[::-1]
                    yield walk[::-1].upper()

        # Diagonal walks
        diagonals = [
            "qaz", "wsx", "edc", "rfv", "tgb", "yhn", "ujm",
            "1qaz", "2wsx", "3edc", "4rfv",
        ]

        for diag in diagonals:
            yield diag
            yield diag.upper()

    def _repeating_patterns(self) -> Iterator[str]:
        """Generate repeating character patterns."""
        chars = string.ascii_lowercase + string.digits

        # Single character repeats
        for char in chars:
            for repeat in range(self.min_length, min(self.max_length + 1, 10)):
                yield char * repeat

        # Two character alternating patterns
        for c1, c2 in itertools.combinations(chars, 2):
            pattern = (c1 + c2) * (self.max_length // 2)
            yield pattern[:self.max_length]

    def _sequential_patterns(self) -> Iterator[str]:
        """Generate sequential patterns."""
        # Number sequences
        for start in range(10):
            for length in range(self.min_length, min(self.max_length + 1, 11)):
                seq = ''.join(str((start + i) % 10) for i in range(length))
                yield seq

        # Alphabet sequences
        for start in range(26):
            for length in range(self.min_length, min(self.max_length + 1, 27)):
                seq = ''.join(chr(ord('a') + (start + i) % 26) for i in range(length))
                yield seq
                yield seq.upper()

    def _date_patterns(self) -> Iterator[str]:
        """Generate date-based patterns."""
        # Common date formats
        for year in range(1950, 2030):
            for month in range(1, 13):
                for day in range(1, 29):  # Simplified
                    yield f"{month:02d}{day:02d}{year}"
                    yield f"{day:02d}{month:02d}{year}"
                    yield f"{year}{month:02d}{day:02d}"
                    yield f"{month:02d}{day:02d}{str(year)[2:]}"

    def _number_suffix_patterns(self) -> Iterator[str]:
        """Generate common words with number suffixes."""
        common_words = [
            "password", "admin", "user", "test", "temp",
            "guest", "demo", "welcome", "login", "pass"
        ]

        for word in common_words:
            # Number suffixes
            for num in range(100):
                yield f"{word}{num}"
                yield f"{word}{num:02d}"

            # Year suffixes
            for year in range(2000, 2030):
                yield f"{word}{year}"
                yield f"{word}{str(year)[2:]}"

            # Special character combinations
            for special in ["!", "@", "#", "$", "123", "!@#"]:
                yield f"{word}{special}"
