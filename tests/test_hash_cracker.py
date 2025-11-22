"""Tests for hash cracking functionality."""

import pytest
from dicti0nary_attack.crackers import HashCracker


class TestHashCracker:
    """Tests for HashCracker."""

    def test_initialization(self):
        """Test cracker initialization."""
        cracker = HashCracker()
        assert cracker.algorithm == 'sha256'

    def test_invalid_algorithm(self):
        """Test invalid algorithm raises error."""
        with pytest.raises(ValueError):
            HashCracker(config={'algorithm': 'invalid'})

    def test_hash_password(self):
        """Test password hashing."""
        password = "test123"
        hash_result = HashCracker.hash_password(password, 'sha256')

        assert isinstance(hash_result, str)
        assert len(hash_result) == 64  # SHA256 produces 64 hex characters

    def test_hash_password_md5(self):
        """Test MD5 hashing."""
        password = "test"
        hash_result = HashCracker.hash_password(password, 'md5')

        assert isinstance(hash_result, str)
        assert len(hash_result) == 32  # MD5 produces 32 hex characters
        assert hash_result == '098f6bcd4621d373cade4e832627b4f6'

    def test_crack_simple_password(self):
        """Test cracking a simple password."""
        password = "test123"
        target_hash = HashCracker.hash_password(password, 'sha256')

        cracker = HashCracker(config={'algorithm': 'sha256'})
        password_gen = iter(["wrong1", "wrong2", "test123", "wrong3"])

        result = cracker.crack(target_hash, password_gen)

        assert result == password

    def test_crack_not_found(self):
        """Test cracking when password is not in wordlist."""
        target_hash = HashCracker.hash_password("notfound", 'sha256')

        cracker = HashCracker(config={'algorithm': 'sha256'})
        password_gen = iter(["wrong1", "wrong2", "wrong3"])

        result = cracker.crack(target_hash, password_gen)

        assert result is None

    def test_crack_with_callback(self):
        """Test cracking with callback function."""
        password = "found"
        target_hash = HashCracker.hash_password(password, 'sha256')

        callback_results = []

        def callback(pwd):
            callback_results.append(pwd)

        cracker = HashCracker(config={'algorithm': 'sha256'})
        password_gen = iter(["test", "found", "other"])

        result = cracker.crack(target_hash, password_gen, callback=callback)

        assert result == password
        assert callback_results == [password]

    def test_stats_tracking(self):
        """Test statistics tracking."""
        target_hash = HashCracker.hash_password("test", 'sha256')

        cracker = HashCracker(config={'algorithm': 'sha256'})
        password_gen = iter(["a", "b", "c", "test"])

        cracker.crack(target_hash, password_gen)

        stats = cracker.get_stats()

        assert stats['attempts'] == 4
        assert stats['matches'] == 1
        assert stats['elapsed_time'] is not None
        assert stats['rate'] is not None

    def test_crack_multiple_hashes(self):
        """Test cracking multiple hashes simultaneously."""
        passwords = ["pass1", "pass2", "pass3"]
        target_hashes = [HashCracker.hash_password(p, 'sha256') for p in passwords]

        cracker = HashCracker(config={'algorithm': 'sha256'})
        password_gen = iter(["wrong", "pass1", "pass2", "pass3", "other"])

        results = cracker.crack_multiple(target_hashes, password_gen)

        assert len(results) == 3
        for hash_val, pwd in results.items():
            assert hash_val in target_hashes
            assert pwd in passwords

    def test_different_algorithms(self):
        """Test different hash algorithms."""
        password = "test"

        algorithms = ['md5', 'sha1', 'sha256', 'sha512']

        for algo in algorithms:
            hash_val = HashCracker.hash_password(password, algo)
            cracker = HashCracker(config={'algorithm': algo})
            password_gen = iter([password])

            result = cracker.crack(hash_val, password_gen)
            assert result == password
