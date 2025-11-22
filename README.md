# 🔐 dicti0nary-attack

> A comprehensive security research utility for testing non-dictionary passwords

Everyone knows that it's easy to crack a password if it appears in a dictionary. **dicti0nary-attack** is a humorous inversion of that concept - it's a powerful tool for generating and testing passwords that are NOT in traditional dictionaries, focusing on the creative variations users think make their passwords "secure."

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![RSR Compliance](https://img.shields.io/badge/RSR-Bronze%20(86%25)-yellow.svg)](RSR_COMPLIANCE.md)
[![Offline-First](https://img.shields.io/badge/offline--first-100%25-green.svg)](RSR_COMPLIANCE.md#5-offline-first--compliant)

## ⚠️ Legal Notice

**This tool is for authorized security testing only.**

Authorized use includes:
- ✅ Penetration testing with explicit written permission
- ✅ Security audits of systems you own
- ✅ CTF (Capture The Flag) competitions
- ✅ Academic research and education
- ✅ Password strength analysis on your own data

Unauthorized access to computer systems is **illegal** and may result in criminal prosecution under computer fraud and abuse laws.

## ✨ Features

### Password Generators

- **Leetspeak Generator**: Transforms words using character substitutions (a→4, e→3, o→0, etc.)
- **Phonetic Generator**: Uses phonetic substitutions (for→4, to→2, you→u)
- **Pattern Generator**: Creates pattern-based passwords (keyboard walks, sequences, date patterns)
- **Random Generator**: Generates truly random non-dictionary passwords
- **Markov Chain Generator**: Statistical password generation based on training data

### Hash Cracking

- **Multi-Algorithm Support**: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, BLAKE2b, BLAKE2s
- **Parallel Processing**: Multi-core support for faster cracking
- **Batch Operations**: Crack multiple hashes simultaneously
- **Progress Tracking**: Real-time statistics and progress monitoring

### Additional Features

- 🎨 **Rich CLI Interface**: Beautiful terminal UI with progress bars and tables
- 🌐 **Web Interface**: Browser-based GUI for easy password generation and cracking
- 📊 **Comprehensive Statistics**: Detailed performance metrics and reporting
- 🔧 **Flexible Configuration**: YAML/JSON configuration files
- 📝 **Multiple Output Formats**: Text, JSON, CSV, HTML reports
- 🐳 **Docker Support**: Containerized deployment
- 🧪 **Extensive Test Suite**: High code coverage with pytest
- ⚡ **Performance Benchmarks**: Built-in benchmarking tools
- 🏆 **RSR Framework Compliant**: Bronze level (86% compliance)
- 📴 **Offline-First**: Core functionality works without internet
- 🔒 **Security-First**: RFC 9116 compliant, comprehensive security policy

## 📦 Installation

### From Source

```bash
git clone https://github.com/Hyperpolymath/dicti0nary-attack.git
cd dicti0nary-attack
pip install -r requirements.txt
pip install -e .
```

### Using Docker

```bash
docker build -t dicti0nary-attack .
docker run --rm dicti0nary-attack dicti0nary --help
```

### Using Docker Compose

```bash
# Run CLI
docker-compose run dicti0nary-cli dicti0nary info

# Run web interface
docker-compose up dicti0nary-web
```

## 🚀 Quick Start

### Generate Passwords

```bash
# Generate 1000 leetspeak passwords
dicti0nary generate -g leetspeak -n 1000

# Save to file
dicti0nary generate -g pattern -n 5000 -o passwords.txt

# Custom length constraints
dicti0nary generate -g random -n 100 --min-length 12 --max-length 20
```

### Crack Password Hashes

```bash
# Crack a SHA256 hash using pattern generator
dicti0nary crack 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 -a sha256 -g pattern

# Use parallel processing
dicti0nary crack <hash> -a sha256 -g leetspeak -p --workers 8

# Use custom wordlist
dicti0nary crack <hash> -a md5 -w wordlists/custom.txt
```

### Create Wordlists

```bash
# Create leetspeak wordlist
dicti0nary create-wordlist wordlists/leetspeak.txt -g leetspeak -n 50000

# Create phonetic wordlist
dicti0nary create-wordlist wordlists/phonetic.txt -g phonetic -n 10000
```

### Hash Passwords

```bash
# Hash with SHA256
dicti0nary hash-password "mypassword"

# Hash with MD5
dicti0nary hash-password "mypassword" -a md5
```

### Run Web Interface

```bash
python -m dicti0nary_attack.web.app

# Or using Make
make run-web
```

Visit http://localhost:5000 in your browser.

## 📚 Documentation

- [Usage Guide](docs/USAGE.md) - Comprehensive usage instructions
- [API Documentation](docs/API.md) - Python API reference
- [Plugin Guide](docs/PLUGINS.md) - Plugin development guide
- [Configuration Guide](config/README.md) - Configuration options
- [RSR Compliance](RSR_COMPLIANCE.md) - Standards compliance report
- [Security Policy](SECURITY.md) - Vulnerability reporting
- [Contributing](CONTRIBUTING.md) - Contribution guidelines

## 🎯 Use Cases

### Security Audit

Test if users are using common non-dictionary password patterns:

```bash
dicti0nary create-wordlist audit.txt -g leetspeak -n 100000
dicti0nary crack <hash> -w audit.txt -a sha256
```

### CTF Competition

Quickly test common patterns:

```bash
dicti0nary crack <ctf_hash> -a md5 -g pattern -p
```

### Password Research

Generate datasets for password strength analysis:

```bash
dicti0nary create-wordlist data/leetspeak.txt -g leetspeak -n 50000
dicti0nary create-wordlist data/phonetic.txt -g phonetic -n 50000
dicti0nary create-wordlist data/patterns.txt -g pattern -n 50000
```

## 🏗️ Architecture

```
dicti0nary-attack/
├── src/dicti0nary_attack/
│   ├── generators/          # Password generation strategies
│   │   ├── base.py          # Base generator class
│   │   ├── leetspeak.py     # Leetspeak transformations
│   │   ├── phonetic.py      # Phonetic substitutions
│   │   ├── pattern.py       # Pattern-based generation
│   │   ├── random_gen.py    # Random generation
│   │   └── markov.py        # Markov chain generation
│   ├── crackers/            # Hash cracking engine
│   │   └── hash_cracker.py  # Multi-algorithm cracker
│   ├── utils/               # Utility modules
│   │   ├── wordlist.py      # Wordlist management
│   │   ├── config.py        # Configuration handling
│   │   └── output.py        # Output formatting
│   ├── web/                 # Web interface
│   │   ├── app.py           # Flask application
│   │   └── templates/       # HTML templates
│   ├── cli.py               # Command-line interface
│   └── benchmark.py         # Performance benchmarks
├── tests/                   # Test suite
├── config/                  # Configuration files
├── docs/                    # Documentation
└── wordlists/              # Example wordlists
```

## 🔧 Configuration

Create a configuration file (`config.yaml`):

```yaml
generators:
  leetspeak:
    max_substitutions: 3
    min_length: 6
    max_length: 16

  pattern:
    min_length: 6
    max_length: 16

cracker:
  algorithm: sha256
  workers: 8
  batch_size: 5000

output:
  format: json
  directory: output
  save_stats: true
```

Use with commands:

```bash
dicti0nary --config config.yaml generate -g leetspeak -n 1000
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dicti0nary_attack --cov-report=html

# Or using Make
make test
```

## 📊 Benchmarks

Run performance benchmarks:

```bash
python -m dicti0nary_attack.benchmark

# Or using Make
make benchmark
```

## 🐳 Docker Usage

### Build Image

```bash
docker build -t dicti0nary-attack .
```

### Run CLI

```bash
docker run --rm dicti0nary-attack dicti0nary generate -g leetspeak -n 100
```

### Run Web Interface

```bash
docker-compose up dicti0nary-web
```

Access at http://localhost:5000

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Hyperpolymath/dicti0nary-attack.git
cd dicti0nary-attack

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt pytest pytest-cov flake8 black
```

### Available Make Commands

```bash
make install       # Install package and dependencies
make test          # Run tests with coverage
make lint          # Run code linters
make clean         # Remove build artifacts
make docker        # Build Docker image
make run-web       # Run web interface
make benchmark     # Run performance benchmarks
```

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `pytest`
2. Code is formatted: `black src/ tests/`
3. No linting errors: `flake8 src/ tests/`
4. Documentation is updated

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for better password security testing tools
- Built with Python, Flask, Rich, and Click
- Thanks to the security research community

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Hyperpolymath/dicti0nary-attack/issues)
- **Documentation**: [docs/](docs/)
- **License**: GPL-3.0

## 🔒 Security Notice

This tool is designed to help security professionals identify weak passwords. It should never be used:

- To gain unauthorized access to any system
- To crack passwords you don't have permission to test
- For any illegal or unethical purposes

Always obtain explicit written permission before testing any system you do not own.

---

**Made with ❤️ for the security research community**
