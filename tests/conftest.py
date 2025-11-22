"""Pytest configuration and fixtures."""

import pytest
import tempfile
import os


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_wordlist(temp_dir):
    """Create a sample wordlist file."""
    wordlist_path = os.path.join(temp_dir, "test_wordlist.txt")
    words = ["password", "test123", "admin", "letmein", "qwerty"]

    with open(wordlist_path, 'w') as f:
        for word in words:
            f.write(f"{word}\n")

    return wordlist_path


@pytest.fixture
def sample_config():
    """Sample configuration dictionary."""
    return {
        'generators': {
            'leetspeak': {
                'max_substitutions': 2,
                'min_length': 4,
                'max_length': 20,
            }
        },
        'cracker': {
            'algorithm': 'sha256',
            'workers': 2,
            'batch_size': 100,
        }
    }
