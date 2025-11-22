"""Tests for utility modules."""

import pytest
import os
import json
import yaml
from dicti0nary_attack.utils.wordlist import WordlistManager
from dicti0nary_attack.utils.config import ConfigManager
from dicti0nary_attack.utils.output import OutputFormatter


class TestWordlistManager:
    """Tests for WordlistManager."""

    def test_load_wordlist(self, sample_wordlist):
        """Test loading a wordlist."""
        manager = WordlistManager()
        words = list(manager.load_wordlist(sample_wordlist))

        assert len(words) == 5
        assert "password" in words
        assert "test123" in words

    def test_save_wordlist(self, temp_dir):
        """Test saving a wordlist."""
        manager = WordlistManager()
        output_path = os.path.join(temp_dir, "output.txt")

        words = iter(["test1", "test2", "test3"])
        manager.save_wordlist(output_path, words)

        # Verify file was created
        assert os.path.exists(output_path)

        # Verify content
        loaded = list(manager.load_wordlist(output_path))
        assert loaded == ["test1", "test2", "test3"]

    def test_save_wordlist_max_words(self, temp_dir):
        """Test saving with max_words limit."""
        manager = WordlistManager()
        output_path = os.path.join(temp_dir, "limited.txt")

        words = iter(["w1", "w2", "w3", "w4", "w5"])
        manager.save_wordlist(output_path, words, max_words=3)

        loaded = list(manager.load_wordlist(output_path))
        assert len(loaded) == 3

    def test_load_dictionary(self, sample_wordlist):
        """Test loading dictionary."""
        manager = WordlistManager()
        manager.load_dictionary(sample_wordlist)

        assert len(manager.dictionary_words) == 5
        assert "password" in manager.dictionary_words

    def test_is_dictionary_word(self, sample_wordlist):
        """Test dictionary word checking."""
        manager = WordlistManager()
        manager.load_dictionary(sample_wordlist)

        assert manager.is_dictionary_word("password")
        assert manager.is_dictionary_word("PASSWORD")  # Case insensitive
        assert not manager.is_dictionary_word("notindict")

    def test_filter_non_dictionary(self, sample_wordlist):
        """Test filtering non-dictionary words."""
        manager = WordlistManager()
        manager.load_dictionary(sample_wordlist)

        words = ["password", "custom123", "admin", "unique"]
        filtered = list(manager.filter_non_dictionary(iter(words)))

        assert "custom123" in filtered
        assert "unique" in filtered
        assert "password" not in filtered
        assert "admin" not in filtered

    def test_merge_wordlists(self, temp_dir):
        """Test merging multiple wordlists."""
        manager = WordlistManager()

        # Create multiple wordlists
        file1 = os.path.join(temp_dir, "list1.txt")
        file2 = os.path.join(temp_dir, "list2.txt")
        output = os.path.join(temp_dir, "merged.txt")

        with open(file1, 'w') as f:
            f.write("word1\nword2\n")

        with open(file2, 'w') as f:
            f.write("word3\nword2\n")  # word2 is duplicate

        manager.merge_wordlists([file1, file2], output, deduplicate=True)

        merged = list(manager.load_wordlist(output))
        assert len(merged) == 3  # Should have 3 unique words
        assert set(merged) == {"word1", "word2", "word3"}


class TestConfigManager:
    """Tests for ConfigManager."""

    def test_default_config(self):
        """Test default configuration."""
        config = ConfigManager()

        assert config.get('cracker.algorithm') == 'sha256'
        assert config.get('generators.leetspeak.max_substitutions') == 3

    def test_load_yaml_config(self, temp_dir):
        """Test loading YAML configuration."""
        config_path = os.path.join(temp_dir, "config.yaml")

        test_config = {
            'cracker': {
                'algorithm': 'md5',
                'workers': 8
            }
        }

        with open(config_path, 'w') as f:
            yaml.dump(test_config, f)

        config = ConfigManager(config_path)

        assert config.get('cracker.algorithm') == 'md5'
        assert config.get('cracker.workers') == 8

    def test_load_json_config(self, temp_dir):
        """Test loading JSON configuration."""
        config_path = os.path.join(temp_dir, "config.json")

        test_config = {
            'cracker': {
                'algorithm': 'sha1',
                'workers': 4
            }
        }

        with open(config_path, 'w') as f:
            json.dump(test_config, f)

        config = ConfigManager(config_path)

        assert config.get('cracker.algorithm') == 'sha1'
        assert config.get('cracker.workers') == 4

    def test_get_with_default(self):
        """Test get with default value."""
        config = ConfigManager()

        assert config.get('nonexistent.key', 'default') == 'default'

    def test_set_value(self):
        """Test setting configuration values."""
        config = ConfigManager()

        config.set('custom.setting', 'value')
        assert config.get('custom.setting') == 'value'

    def test_save_config(self, temp_dir):
        """Test saving configuration."""
        config = ConfigManager()
        config.set('test.value', 123)

        save_path = os.path.join(temp_dir, "saved.yaml")
        config.save_config(save_path)

        # Load and verify
        loaded = ConfigManager(save_path)
        assert loaded.get('test.value') == 123

    def test_get_generator_config(self):
        """Test getting generator-specific config."""
        config = ConfigManager()

        leetspeak_config = config.get_generator_config('leetspeak')

        assert 'max_substitutions' in leetspeak_config
        assert leetspeak_config['max_substitutions'] == 3

    def test_get_cracker_config(self):
        """Test getting cracker config."""
        config = ConfigManager()

        cracker_config = config.get_cracker_config()

        assert 'algorithm' in cracker_config
        assert cracker_config['algorithm'] == 'sha256'


class TestOutputFormatter:
    """Tests for OutputFormatter."""

    def test_initialization(self, temp_dir):
        """Test output formatter initialization."""
        output_dir = os.path.join(temp_dir, "output")
        formatter = OutputFormatter(output_dir)

        assert os.path.exists(output_dir)

    def test_save_passwords_text(self, temp_dir):
        """Test saving passwords as text."""
        formatter = OutputFormatter(temp_dir)
        passwords = ["pass1", "pass2", "pass3"]

        formatter.save_passwords(passwords, "passwords.txt", format='text')

        output_file = os.path.join(temp_dir, "passwords.txt")
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            content = f.read().strip().split('\n')

        assert content == passwords

    def test_save_passwords_json(self, temp_dir):
        """Test saving passwords as JSON."""
        formatter = OutputFormatter(temp_dir)
        passwords = ["pass1", "pass2", "pass3"]

        formatter.save_passwords(passwords, "passwords.json", format='json')

        output_file = os.path.join(temp_dir, "passwords.json")
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            data = json.load(f)

        assert data['passwords'] == passwords

    def test_save_passwords_csv(self, temp_dir):
        """Test saving passwords as CSV."""
        formatter = OutputFormatter(temp_dir)
        passwords = ["pass1", "pass2", "pass3"]

        formatter.save_passwords(passwords, "passwords.csv", format='csv')

        output_file = os.path.join(temp_dir, "passwords.csv")
        assert os.path.exists(output_file)

    def test_save_stats(self, temp_dir):
        """Test saving statistics."""
        formatter = OutputFormatter(temp_dir)
        stats = {
            'attempts': 100,
            'matches': 5,
            'rate': 25.5
        }

        formatter.save_stats(stats, "stats.json")

        output_file = os.path.join(temp_dir, "stats.json")
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            loaded_stats = json.load(f)

        assert loaded_stats['attempts'] == 100
        assert loaded_stats['matches'] == 5

    def test_generate_html_report(self, temp_dir):
        """Test generating HTML report."""
        formatter = OutputFormatter(temp_dir)
        stats = {
            'total_passwords': 1000,
            'time_elapsed': 5.5
        }

        formatter.generate_html_report(
            "Test Report",
            stats,
            filename="report.html"
        )

        output_file = os.path.join(temp_dir, "report.html")
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            content = f.read()

        assert "Test Report" in content
        assert "total_passwords" in content.lower()

    def test_save_cracking_results(self, temp_dir):
        """Test saving cracking results."""
        formatter = OutputFormatter(temp_dir)
        results = {
            'hash1': 'password1',
            'hash2': 'password2'
        }
        stats = {
            'attempts': 50,
            'matches': 2
        }

        formatter.save_cracking_results(results, stats)

        output_file = os.path.join(temp_dir, "cracking_results.json")
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            data = json.load(f)

        assert 'results' in data
        assert 'stats' in data
        assert len(data['results']) == 2
