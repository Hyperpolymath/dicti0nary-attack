"""Wordlist management and filtering."""

import os
from typing import Iterator, Optional, List, Set
import logging

logger = logging.getLogger(__name__)


class WordlistManager:
    """Manages wordlists for password generation and filtering."""

    def __init__(self, wordlist_dir: Optional[str] = None):
        """
        Initialize the wordlist manager.

        Args:
            wordlist_dir: Directory containing wordlists
        """
        self.wordlist_dir = wordlist_dir or "wordlists"
        self.dictionary_words: Set[str] = set()

    def load_dictionary(self, filepath: str):
        """
        Load a dictionary file.

        Args:
            filepath: Path to dictionary file
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self.dictionary_words.add(word)

            logger.info(f"Loaded {len(self.dictionary_words)} dictionary words from {filepath}")
        except FileNotFoundError:
            logger.warning(f"Dictionary file not found: {filepath}")
        except Exception as e:
            logger.error(f"Error loading dictionary: {e}")

    def is_dictionary_word(self, word: str) -> bool:
        """
        Check if a word is in the dictionary.

        Args:
            word: Word to check

        Returns:
            True if word is in dictionary
        """
        return word.lower() in self.dictionary_words

    def load_wordlist(self, filepath: str) -> Iterator[str]:
        """
        Load and iterate through a wordlist file.

        Args:
            filepath: Path to wordlist file

        Yields:
            Words from the wordlist
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        yield word
        except FileNotFoundError:
            logger.error(f"Wordlist file not found: {filepath}")
        except Exception as e:
            logger.error(f"Error loading wordlist: {e}")

    def save_wordlist(self, filepath: str, words: Iterator[str], max_words: Optional[int] = None):
        """
        Save words to a wordlist file.

        Args:
            filepath: Path to output file
            words: Iterator of words to save
            max_words: Maximum number of words to save
        """
        try:
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                count = 0
                for word in words:
                    f.write(f"{word}\n")
                    count += 1

                    if max_words and count >= max_words:
                        break

            logger.info(f"Saved {count} words to {filepath}")
        except Exception as e:
            logger.error(f"Error saving wordlist: {e}")

    def filter_non_dictionary(self, words: Iterator[str]) -> Iterator[str]:
        """
        Filter out dictionary words from a word iterator.

        Args:
            words: Iterator of words to filter

        Yields:
            Non-dictionary words
        """
        for word in words:
            if not self.is_dictionary_word(word):
                yield word

    def merge_wordlists(self, filepaths: List[str], output_path: str, deduplicate: bool = True):
        """
        Merge multiple wordlists into one.

        Args:
            filepaths: List of input wordlist paths
            output_path: Path to output merged wordlist
            deduplicate: Whether to remove duplicates
        """
        seen: Set[str] = set() if deduplicate else None
        count = 0

        try:
            with open(output_path, 'w', encoding='utf-8') as out:
                for filepath in filepaths:
                    for word in self.load_wordlist(filepath):
                        if deduplicate:
                            if word in seen:
                                continue
                            seen.add(word)

                        out.write(f"{word}\n")
                        count += 1

            logger.info(f"Merged {len(filepaths)} wordlists into {output_path} ({count} words)")
        except Exception as e:
            logger.error(f"Error merging wordlists: {e}")
