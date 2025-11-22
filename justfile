# justfile - Command runner for dicti0nary-attack
# https://github.com/casey/just

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025 Security Research Team

# Default recipe - show available commands
default:
    @just --list

# Install dependencies
install:
    pip install -r requirements.txt
    pip install -e .

# Install development dependencies
install-dev:
    pip install -r requirements.txt
    pip install -e .
    pip install pytest pytest-cov flake8 black isort mypy bandit safety

# Run all tests
test:
    pytest tests/ -v

# Run tests with coverage
test-cov:
    pytest tests/ -v --cov=dicti0nary_attack --cov-report=html --cov-report=term-missing

# Run tests in watch mode
test-watch:
    pytest-watch tests/

# Lint code with flake8
lint:
    flake8 src/ tests/ --max-line-length=127 --exclude=__pycache__,.venv,venv

# Format code with black
format:
    black src/ tests/
    isort src/ tests/

# Type check with mypy
typecheck:
    mypy src/dicti0nary_attack/ --ignore-missing-imports

# Run security checks
security:
    bandit -r src/
    safety check

# Run all quality checks
check: lint typecheck security test

# Clean build artifacts
clean:
    rm -rf build/ dist/ *.egg-info/
    rm -rf .pytest_cache/ .coverage htmlcov/
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete

# Clean output files
clean-output:
    rm -rf output/*.log output/*.csv output/*.json output/*.html

# Build Docker image
docker-build:
    docker build -t dicti0nary-attack:latest .

# Run Docker container (CLI)
docker-run:
    docker run --rm -it dicti0nary-attack:latest dicti0nary --help

# Run Docker web interface
docker-web:
    docker-compose up dicti0nary-web

# Stop Docker containers
docker-stop:
    docker-compose down

# Run benchmarks
benchmark:
    python -m dicti0nary_attack.benchmark

# Generate passwords (quick test)
generate count="100" generator="leetspeak":
    python -m dicti0nary_attack.cli generate -g {{generator}} -n {{count}}

# Run web interface
web:
    python -m dicti0nary_attack.web.app

# Validate RSR compliance
validate-rsr:
    @echo "Checking RSR compliance..."
    @echo "✓ Checking documentation files..."
    @test -f README.md && echo "  ✓ README.md"
    @test -f LICENSE && echo "  ✓ LICENSE"
    @test -f CONTRIBUTING.md && echo "  ✓ CONTRIBUTING.md"
    @test -f CODE_OF_CONDUCT.md && echo "  ✓ CODE_OF_CONDUCT.md"
    @test -f SECURITY.md && echo "  ✓ SECURITY.md"
    @test -f CHANGELOG.md && echo "  ✓ CHANGELOG.md"
    @test -f MAINTAINERS.md && echo "  ✓ MAINTAINERS.md"
    @echo "✓ Checking .well-known directory..."
    @test -f .well-known/security.txt && echo "  ✓ security.txt"
    @test -f .well-known/ai.txt && echo "  ✓ ai.txt"
    @test -f .well-known/humans.txt && echo "  ✓ humans.txt"
    @echo "✓ Checking build system..."
    @test -f Makefile && echo "  ✓ Makefile"
    @test -f justfile && echo "  ✓ justfile"
    @test -f Dockerfile && echo "  ✓ Dockerfile"
    @test -f docker-compose.yml && echo "  ✓ docker-compose.yml"
    @test -f .github/workflows/ci.yml && echo "  ✓ CI/CD"
    @echo "✓ Running tests..."
    @pytest tests/ -v --tb=short
    @echo ""
    @echo "✅ RSR Compliance Check Complete!"
    @echo "See RSR_COMPLIANCE.md for detailed compliance report"

# Validate offline-first operation
validate-offline:
    @echo "Validating offline-first operation..."
    @echo "Checking core generators (no network calls)..."
    @! grep -r "requests\|urllib\|http\.client" src/dicti0nary_attack/generators/ || (echo "❌ Network calls found in generators!" && exit 1)
    @echo "✓ Generators are offline-first"
    @! grep -r "requests\|urllib\|http\.client" src/dicti0nary_attack/crackers/ || (echo "❌ Network calls found in crackers!" && exit 1)
    @echo "✓ Crackers are offline-first"
    @echo "✅ Offline-first validation passed!"

# Create a new release
release version:
    @echo "Creating release v{{version}}..."
    @echo "Updating version in setup.py..."
    @sed -i 's/version="[^"]*"/version="{{version}}"/' setup.py
    @echo "Updating version in __init__.py..."
    @sed -i 's/__version__ = "[^"]*"/__version__ = "{{version}}"/' src/dicti0nary_attack/__init__.py
    @echo "Running tests..."
    @pytest tests/ -v
    @echo "Building package..."
    @python setup.py sdist bdist_wheel
    @echo "Creating git tag..."
    @git tag -a "v{{version}}" -m "Release v{{version}}"
    @echo "✅ Release v{{version}} ready!"
    @echo "Next steps:"
    @echo "  1. git push origin v{{version}}"
    @echo "  2. Create GitHub release"
    @echo "  3. twine upload dist/*"

# Show project statistics
stats:
    @echo "dicti0nary-attack Project Statistics"
    @echo "===================================="
    @echo ""
    @echo "Lines of Code:"
    @find src/ -name "*.py" | xargs wc -l | tail -1
    @echo ""
    @echo "Test Files:"
    @find tests/ -name "test_*.py" | wc -l
    @echo ""
    @echo "Test Count:"
    @grep -r "def test_" tests/ | wc -l
    @echo ""
    @echo "Documentation Files:"
    @find . -maxdepth 2 -name "*.md" | wc -l
    @echo ""
    @echo "Dependencies:"
    @cat requirements.txt | grep -v "^#" | wc -l

# Run code quality analysis
quality:
    @echo "Code Quality Analysis"
    @echo "===================="
    @echo ""
    @echo "Linting..."
    @flake8 src/ tests/ --statistics --count || true
    @echo ""
    @echo "Type Checking..."
    @mypy src/dicti0nary_attack/ --ignore-missing-imports --show-error-codes || true
    @echo ""
    @echo "Security Scanning..."
    @bandit -r src/ -f json -o bandit-report.json || true
    @echo ""
    @echo "Dependency Security..."
    @safety check || true

# Generate documentation
docs:
    @echo "Documentation is in docs/ directory"
    @echo "Available docs:"
    @ls -1 docs/

# Create wordlist
wordlist path generator="leetspeak" count="10000":
    python -m dicti0nary_attack.cli create-wordlist {{path}} -g {{generator}} -n {{count}}

# Hash a password for testing
hash password algorithm="sha256":
    python -m dicti0nary_attack.cli hash-password "{{password}}" -a {{algorithm}}

# Quick crack demo (educational)
demo-crack:
    @echo "Demo: Cracking a simple hash"
    @HASH=$(python -c "from dicti0nary_attack.crackers import HashCracker; print(HashCracker.hash_password('password123', 'sha256'))")
    @echo "Hash: $$HASH"
    @echo "Attempting to crack..."
    @python -m dicti0nary_attack.cli crack $$HASH -a sha256 -g pattern

# Show info about generators and algorithms
info:
    python -m dicti0nary_attack.cli info

# Setup pre-commit hooks
setup-hooks:
    @echo "Setting up pre-commit hooks..."
    @echo "#!/bin/sh" > .git/hooks/pre-commit
    @echo "just lint" >> .git/hooks/pre-commit
    @echo "just test" >> .git/hooks/pre-commit
    @chmod +x .git/hooks/pre-commit
    @echo "✅ Pre-commit hooks installed"

# Initialize development environment
init: install-dev setup-hooks
    @echo "✅ Development environment initialized"
    @echo "Run 'just' to see available commands"
