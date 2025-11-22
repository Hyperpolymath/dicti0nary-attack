"""Markov chain password generator."""

import random
from typing import Iterator, Optional, Dict, Any, List
from collections import defaultdict
from dicti0nary_attack.generators.base import PasswordGenerator


class MarkovGenerator(PasswordGenerator):
    """
    Generates passwords using Markov chains trained on example passwords.

    Creates statistically similar but non-identical passwords based on
    patterns learned from a training set.
    """

    def __init__(self, training_data: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Markov generator.

        Args:
            training_data: List of passwords/words to train on
            config: Configuration dictionary
        """
        super().__init__(config)
        self.order = self.config.get("order", 2)  # N-gram order
        self.min_length = self.config.get("min_length", 6)
        self.max_length = self.config.get("max_length", 16)

        self.chain: Dict[str, List[str]] = defaultdict(list)
        self.start_tokens: List[str] = []

        if training_data:
            self.train(training_data)

    def train(self, data: List[str]):
        """
        Train the Markov chain on password data.

        Args:
            data: List of passwords/words to learn from
        """
        for text in data:
            # Add start marker
            padded = "^" * self.order + text + "$"

            # Build n-gram chain
            for i in range(len(padded) - self.order):
                state = padded[i:i + self.order]
                next_char = padded[i + self.order]

                self.chain[state].append(next_char)

                # Track valid start states
                if state.startswith("^"):
                    self.start_tokens.append(state)

    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate passwords using the Markov chain.

        Args:
            count: Number of passwords to generate

        Yields:
            Generated passwords
        """
        if not self.chain:
            # Use default training data if not trained
            self._default_training()

        generated = 0

        while count is None or generated < count:
            password = self._generate_one()

            if password and self.apply_filters(password):
                self.stats["generated"] += 1
                generated += 1
                yield password

    def _generate_one(self) -> Optional[str]:
        """Generate a single password."""
        if not self.start_tokens:
            return None

        # Start with random start token
        current = random.choice(self.start_tokens)
        result = []
        max_iterations = self.max_length * 2

        for _ in range(max_iterations):
            if current not in self.chain:
                break

            # Choose next character
            next_char = random.choice(self.chain[current])

            if next_char == "$":  # End marker
                break

            if next_char != "^":  # Skip start markers
                result.append(next_char)

            # Update state
            current = current[1:] + next_char

            if len(result) >= self.max_length:
                break

        password = ''.join(result)

        if len(password) < self.min_length:
            return None

        return password

    def _default_training(self):
        """Train on default password patterns."""
        default_patterns = [
            "password123", "letmein1", "welcome99", "admin2023",
            "qwerty456", "dragon88", "monkey123", "master2024",
            "shadow777", "superman1", "baseball99", "football2023",
            "trustno1", "access123", "whatever99", "princess1",
            "starwars2023", "ranger99", "batman123", "wizard777"
        ]

        self.train(default_patterns)
