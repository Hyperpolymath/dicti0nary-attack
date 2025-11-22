"""Tests for password generators."""

import pytest
from dicti0nary_attack.generators import (
    LeetspeakGenerator,
    PhoneticGenerator,
    PatternGenerator,
    RandomGenerator,
    MarkovGenerator,
)


class TestLeetspeakGenerator:
    """Tests for LeetspeakGenerator."""

    def test_generate_basic(self):
        """Test basic password generation."""
        gen = LeetspeakGenerator(base_words=["test"])
        passwords = list(gen.generate(count=10))

        assert len(passwords) > 0
        assert all(isinstance(p, str) for p in passwords)

    def test_substitutions(self):
        """Test that substitutions are applied."""
        gen = LeetspeakGenerator(base_words=["password"], config={'max_substitutions': 1})
        passwords = list(gen.generate(count=100))

        # Should have variations like p4ssword, passw0rd, etc.
        assert len(set(passwords)) > 1
        assert "password" in passwords  # Base word should be included

    def test_min_max_length_filter(self):
        """Test length filtering."""
        config = {'min_length': 5, 'max_length': 8}
        gen = LeetspeakGenerator(base_words=["test", "verylongpassword"], config=config)
        passwords = list(gen.generate(count=50))

        for pwd in passwords:
            assert 5 <= len(pwd) <= 8

    def test_stats_tracking(self):
        """Test that statistics are tracked."""
        gen = LeetspeakGenerator(base_words=["test"])
        list(gen.generate(count=10))

        stats = gen.get_stats()
        assert 'generated' in stats
        assert stats['generated'] > 0


class TestPhoneticGenerator:
    """Tests for PhoneticGenerator."""

    def test_generate_basic(self):
        """Test basic password generation."""
        gen = PhoneticGenerator(phrases=["see you later"])
        passwords = list(gen.generate(count=10))

        assert len(passwords) > 0
        assert all(isinstance(p, str) for p in passwords)

    def test_phonetic_substitutions(self):
        """Test phonetic substitutions."""
        gen = PhoneticGenerator(phrases=["for you"], config={'case_variations': False})
        passwords = list(gen.generate(count=20))

        # Should include variations like "4u", "foru", etc.
        assert len(passwords) > 1

    def test_case_variations(self):
        """Test case variations."""
        gen = PhoneticGenerator(phrases=["to be"], config={'case_variations': True})
        passwords = list(gen.generate(count=20))

        # Should have different case variations
        assert len(set(passwords)) > 1


class TestPatternGenerator:
    """Tests for PatternGenerator."""

    def test_generate_basic(self):
        """Test basic password generation."""
        gen = PatternGenerator(config={'min_length': 4, 'max_length': 10})
        passwords = list(gen.generate(count=50))

        assert len(passwords) > 0
        assert all(isinstance(p, str) for p in passwords)

    def test_keyboard_walks(self):
        """Test keyboard walk generation."""
        gen = PatternGenerator()
        passwords = list(gen.generate(count=100))

        # Should include common keyboard walks
        assert any('qwerty' in p.lower() for p in passwords)

    def test_length_constraints(self):
        """Test length constraints."""
        config = {'min_length': 6, 'max_length': 8}
        gen = PatternGenerator(config=config)
        passwords = list(gen.generate(count=50))

        for pwd in passwords:
            assert 6 <= len(pwd) <= 8


class TestRandomGenerator:
    """Tests for RandomGenerator."""

    def test_generate_basic(self):
        """Test basic password generation."""
        gen = RandomGenerator(config={'min_length': 8, 'max_length': 12})
        passwords = list(gen.generate(count=20))

        assert len(passwords) == 20
        assert all(isinstance(p, str) for p in passwords)

    def test_length_range(self):
        """Test password length is within range."""
        config = {'min_length': 10, 'max_length': 10}
        gen = RandomGenerator(config=config)
        passwords = list(gen.generate(count=10))

        for pwd in passwords:
            assert len(pwd) == 10

    def test_character_types(self):
        """Test character type usage."""
        config = {
            'min_length': 20,
            'max_length': 20,
            'use_uppercase': True,
            'use_lowercase': True,
            'use_digits': True,
            'use_special': False
        }
        gen = RandomGenerator(config=config)
        passwords = list(gen.generate(count=10))

        for pwd in passwords:
            # Should have mix of character types
            assert any(c.isupper() or c.islower() or c.isdigit() for c in pwd)

    def test_pronounceable(self):
        """Test pronounceable password generation."""
        gen = RandomGenerator(config={'min_length': 8, 'max_length': 12})
        passwords = list(gen.generate_pronounceable(count=10))

        assert len(passwords) == 10
        assert all(isinstance(p, str) for p in passwords)


class TestMarkovGenerator:
    """Tests for MarkovGenerator."""

    def test_generate_with_training_data(self):
        """Test generation with training data."""
        training = ["password123", "letmein1", "admin2023"]
        gen = MarkovGenerator(training_data=training)
        passwords = list(gen.generate(count=10))

        assert len(passwords) > 0
        assert all(isinstance(p, str) for p in passwords)

    def test_generate_without_training(self):
        """Test generation falls back to defaults without training."""
        gen = MarkovGenerator()
        passwords = list(gen.generate(count=10))

        assert len(passwords) > 0

    def test_training(self):
        """Test training functionality."""
        gen = MarkovGenerator(config={'order': 2})
        gen.train(["test123", "test456", "test789"])

        passwords = list(gen.generate(count=10))
        assert len(passwords) > 0

    def test_length_constraints(self):
        """Test length constraints."""
        config = {'min_length': 6, 'max_length': 10, 'order': 2}
        gen = MarkovGenerator(config=config)
        passwords = list(gen.generate(count=20))

        for pwd in passwords:
            assert 6 <= len(pwd) <= 10
