"""Random non-dictionary password generator."""

import random
import string
from typing import Iterator, Optional, Dict, Any, Set
from dicti0nary_attack.generators.base import PasswordGenerator


class RandomGenerator(PasswordGenerator):
    """
    Generates random passwords that avoid dictionary words.

    Creates truly random combinations that are statistically unlikely
    to appear in any dictionary.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the random generator.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.min_length = self.config.get("min_length", 8)
        self.max_length = self.config.get("max_length", 16)
        self.use_uppercase = self.config.get("use_uppercase", True)
        self.use_lowercase = self.config.get("use_lowercase", True)
        self.use_digits = self.config.get("use_digits", True)
        self.use_special = self.config.get("use_special", True)

        self.charset = self._build_charset()
        self.generated_set: Set[str] = set()

    def _build_charset(self) -> str:
        """Build character set based on configuration."""
        charset = ""
        if self.use_lowercase:
            charset += string.ascii_lowercase
        if self.use_uppercase:
            charset += string.ascii_uppercase
        if self.use_digits:
            charset += string.digits
        if self.use_special:
            charset += string.punctuation

        return charset

    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate random passwords.

        Args:
            count: Number of passwords to generate

        Yields:
            Random password strings
        """
        if not self.charset:
            raise ValueError("No character types enabled")

        generated = 0
        max_attempts = (count or 1000) * 10  # Prevent infinite loops
        attempts = 0

        while (count is None or generated < count) and attempts < max_attempts:
            attempts += 1

            # Random length within range
            length = random.randint(self.min_length, self.max_length)

            # Generate random password
            password = ''.join(random.choices(self.charset, k=length))

            # Avoid duplicates
            if password in self.generated_set:
                continue

            if self.apply_filters(password):
                self.generated_set.add(password)
                self.stats["generated"] += 1
                generated += 1
                yield password

    def generate_pronounceable(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate pronounceable but non-dictionary passwords.

        Args:
            count: Number of passwords to generate

        Yields:
            Pronounceable random passwords
        """
        # Consonants and vowels for pronounceable generation
        vowels = "aeiou"
        consonants = "bcdfghjklmnprstvwxyz"

        generated = 0

        while count is None or generated < count:
            length = random.randint(self.min_length, self.max_length)
            password = []

            for i in range(length):
                if i % 2 == 0:
                    password.append(random.choice(consonants))
                else:
                    password.append(random.choice(vowels))

            # Add random digit if configured
            if self.use_digits and random.random() < 0.5:
                password.append(str(random.randint(0, 9)))

            password_str = ''.join(password)

            # Random capitalization
            if self.use_uppercase:
                password_str = ''.join(
                    c.upper() if random.random() < 0.3 else c
                    for c in password_str
                )

            if password_str not in self.generated_set and self.apply_filters(password_str):
                self.generated_set.add(password_str)
                self.stats["generated"] += 1
                generated += 1
                yield password_str
