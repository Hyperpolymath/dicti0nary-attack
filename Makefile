.PHONY: help install test lint clean docker run-web benchmark

help:
	@echo "dicti0nary-attack - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  install       - Install package and dependencies"
	@echo "  test          - Run tests with coverage"
	@echo "  lint          - Run code linters"
	@echo "  clean         - Remove build artifacts"
	@echo "  docker        - Build Docker image"
	@echo "  docker-run    - Run Docker container"
	@echo "  run-web       - Run web interface"
	@echo "  benchmark     - Run performance benchmarks"
	@echo "  docs          - Build documentation"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=dicti0nary_attack --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	pylint src/dicti0nary_attack/

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + || true
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage
	rm -rf output/*.log output/*.csv output/*.json

docker:
	docker build -t dicti0nary-attack:latest .

docker-run:
	docker run --rm -it dicti0nary-attack:latest dicti0nary --help

docker-web:
	docker-compose up dicti0nary-web

run-web:
	python -m dicti0nary_attack.web.app

benchmark:
	python -m dicti0nary_attack.benchmark

docs:
	@echo "Documentation files:"
	@ls -lh docs/

format:
	black src/ tests/
	isort src/ tests/

security:
	bandit -r src/
	safety check
