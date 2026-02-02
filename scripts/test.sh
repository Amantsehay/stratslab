#!/bin/bash
# Run test suite with coverage
# Executes all tests and generates a coverage report

set -e

echo "Running test suite with coverage..."
poetry run pytest tests/ -v --cov=stratslabapi --cov-report=term-missing
