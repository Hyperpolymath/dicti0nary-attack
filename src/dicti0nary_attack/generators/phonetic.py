"""Phonetic password generator."""

from typing import Iterator, Optional, Dict, Any, List
from dicti0nary_attack.generators.base import PasswordGenerator
import itertools


class PhoneticGenerator(PasswordGenerator):
    """
    Generates passwords based on phonetic substitutions.

    Targets passwords where users substitute words/syllables with
    phonetically similar alternatives (e.g., "for" -> "4", "ate" -> "8").
    """

    PHONETIC_SUBSTITUTIONS = {
        'for': ['4', 'for', 'four'],
        'to': ['2', 'to', 'too'],
        'too': ['2', 'to', 'too'],
        'ate': ['8', 'ate', 'eight'],
        'you': ['u', 'you', 'yu'],
        'are': ['r', 'are'],
        'see': ['c', 'see', 'sea'],
        'be': ['b', 'be', 'bee'],
        'why': ['y', 'why'],
        'eye': ['i', 'eye'],
        'won': ['1', 'won', 'one'],
        'one': ['1', 'won', 'one'],
        'too': ['2', 'too', 'two'],
        'two': ['2', 'too', 'two'],
        'tea': ['t', 'tea'],
        'sea': ['c', 'see', 'sea'],
        'bee': ['b', 'be', 'bee'],
        'oh': ['0', 'oh', 'o'],
        'kay': ['k', 'kay', 'ok'],
    }

    # Common phrases to transform
    DEFAULT_PHRASES = [
        "see you later",
        "be right back",
        "are you okay",
        "for you",
        "to be or not to be",
        "want to play",
        "see you soon",
        "easy as one two three",
    ]

    def __init__(self, phrases: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the phonetic generator.

        Args:
            phrases: List of phrases to transform
            config: Configuration dictionary
        """
        super().__init__(config)
        self.phrases = phrases or self.DEFAULT_PHRASES
        self.case_variations = self.config.get("case_variations", True)

    def generate(self, count: Optional[int] = None) -> Iterator[str]:
        """
        Generate phonetic password variations.

        Args:
            count: Maximum number of passwords to generate

        Yields:
            Phonetic password variations
        """
        generated = 0

        for phrase in self.phrases:
            if count and generated >= count:
                break

            words = phrase.lower().split()

            # Find all substitutable words
            substitutions = []
            for word in words:
                if word in self.PHONETIC_SUBSTITUTIONS:
                    substitutions.append(self.PHONETIC_SUBSTITUTIONS[word])
                else:
                    substitutions.append([word])

            # Generate all combinations
            for combo in itertools.product(*substitutions):
                if count and generated >= count:
                    break

                password = ''.join(combo)

                if self.apply_filters(password):
                    self.stats["generated"] += 1
                    generated += 1
                    yield password

                    # Generate case variations
                    if self.case_variations:
                        for variation in self._case_variations(password):
                            if count and generated >= count:
                                break
                            if self.apply_filters(variation):
                                self.stats["generated"] += 1
                                generated += 1
                                yield variation

    def _case_variations(self, text: str) -> Iterator[str]:
        """
        Generate case variations of text.

        Args:
            text: Input text

        Yields:
            Case variations (capitalize first, all caps, etc.)
        """
        variations = [
            text.capitalize(),
            text.upper(),
            text.title(),
        ]

        for var in variations:
            if var != text:
                yield var
