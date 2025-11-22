"""Leetspeak password generator."""

import itertools
from typing import Iterator, Optional, Dict, Any, List
from dicti0nary_attack.generators.base import PasswordGenerator


class LeetspeakGenerator(PasswordGenerator):
    """
    Generates passwords using leetspeak transformations.

    Converts normal characters to their leetspeak equivalents and generates
    all possible combinations. This targets passwords where users think they're
    being clever by using "P@ssw0rd" instead of "Password".
    """

    # Standard leetspeak character mappings
    LEET_MAP = {
        'a': ['a', '4', '@', 'A'],
        'e': ['e', '3', 'E'],
        'i': ['i', '1', '!', '|', 'I'],
        'o': ['o', '0', 'O'],
        's': ['s', '5', '$', 'S'],
        't': ['t', '7', '+', 'T'],
        'l': ['l', '1', '|', 'L'],
        'g': ['g', '9', 'G'],
        'b': ['b', '8', 'B'],
        'z': ['z', '2', 'Z'],
    }

    def __init__(self, base_words: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the leetspeak generator.

        Args:
            base_words: List of base words to transform
            config: Configuration dictionary
        """
        super().__init__(config)
        self.base_words = base_words or self._default_base_words()
        self.max_substitutions = self.config.get("max_substitutions", 3)

    def _default_base_words(self) -> List[str]:
        """Generate default base words."""
        # Common password patterns
        return [
            "password", "welcome", "admin", "login", "letmein",
            "qwerty", "monkey", "dragon", "master", "trustno",
            "baseball", "football", "access", "shadow", "superman"
        ]

    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate leetspeak variations.

        Args:
            count: Maximum number of passwords to generate

        Yields:
            Leetspeak password variations
        """
        generated = 0

        for word in self.base_words:
            if count and generated >= count:
                break

            # Generate all possible leetspeak variations
            for variation in self._generate_variations(word):
                if count and generated >= count:
                    break

                if self.apply_filters(variation):
                    self.stats["generated"] += 1
                    generated += 1
                    yield variation

    def _generate_variations(self, word: str) -> Iterator[str]:
        """
        Generate all leetspeak variations of a word.

        Args:
            word: Base word to transform

        Yields:
            Leetspeak variations
        """
        word_lower = word.lower()

        # Find positions where substitutions can be made
        substitutable_positions = []
        for i, char in enumerate(word_lower):
            if char in self.LEET_MAP:
                substitutable_positions.append((i, char))

        # Limit number of simultaneous substitutions
        max_subs = min(self.max_substitutions, len(substitutable_positions))

        # Generate combinations with different numbers of substitutions
        for num_subs in range(max_subs + 1):
            for positions in itertools.combinations(substitutable_positions, num_subs):
                # For each combination, generate all possible character choices
                if not positions:
                    yield word
                    continue

                char_options = [self.LEET_MAP[char] for _, char in positions]

                for char_combo in itertools.product(*char_options):
                    result = list(word_lower)
                    for (pos, _), new_char in zip(positions, char_combo):
                        result[pos] = new_char
                    yield ''.join(result)

    def add_base_words(self, words: List[str]):
        """
        Add more base words to transform.

        Args:
            words: Additional base words
        """
        self.base_words.extend(words)
