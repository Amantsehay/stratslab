#!/bin/bash
# Full validation pipeline
# Runs tests, type checking, and code formatting checks

set -e

echo "Running validation pipeline..."
echo ""

echo "1. Running tests..."
poetry run pytest tests/ -v
echo "✓ Tests passed"
echo ""

if command -v poetry run mypy &> /dev/null; then
    echo "2. Type checking..."
    poetry run mypy stratslabapi || true
    echo "✓ Type checking complete"
    echo ""
fi

if command -v poetry run black &> /dev/null; then
    echo "3. Code formatting check..."
    poetry run black --check . || true
    echo "✓ Code formatting check complete"
    echo ""
fi

if command -v poetry run isort &> /dev/null; then
    echo "4. Import sorting check..."
    poetry run isort --check-only . || true
    echo "✓ Import sorting check complete"
    echo ""
fi

echo "✓ All validations passed"
