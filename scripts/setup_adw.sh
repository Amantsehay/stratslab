#!/bin/bash

# ADW Setup Script - Configure environment for agentic developer workflows

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "========================================="
echo "ADW Environment Setup"
echo "========================================="
echo ""

# Check prerequisites
echo "✓ Checking prerequisites..."

# Check for gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Install from: https://cli.github.com/"
    exit 1
fi
echo "✓ GitHub CLI found: $(gh --version)"

# Check for Claude Code CLI
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI is not installed"
    echo "Install from: https://docs.anthropic.com/en/docs/claude-code"
    exit 1
fi
echo "✓ Claude Code CLI found: $(claude --version)"

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "❌ uv package manager is not installed"
    echo "Install from: https://astral.sh/uv/install"
    exit 1
fi
echo "✓ uv found: $(uv --version)"

# Check for git
if ! command -v git &> /dev/null; then
    echo "❌ git is not installed"
    exit 1
fi
echo "✓ git found: $(git --version)"

echo ""
echo "✓ All prerequisites installed!"
echo ""

# Check GitHub authentication
echo "Checking GitHub authentication..."
if gh auth status &>/dev/null; then
    echo "✓ GitHub CLI authenticated"
else
    echo "⚠ GitHub CLI not authenticated"
    echo "Run: gh auth login"
fi

echo ""

# Environment variables
echo "Setting up environment variables..."
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Creating .env from .env.example..."
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        cp "$SCRIPT_DIR/.env.example" "$ENV_FILE"
        echo "✓ .env created from .env.example"
        echo ""
        echo "⚠ Please configure the following in .env:"
        echo "  - GITHUB_REPO_URL"
        echo "  - ANTHROPIC_API_KEY"
        echo "  - DATABASE_URL (if using database tracking)"
    else
        echo "❌ .env.example not found"
        exit 1
    fi
else
    echo "✓ .env file already exists"
fi

echo ""

# Verify ADW directory
ADW_DIR="$SCRIPT_DIR/adws"
if [ ! -d "$ADW_DIR" ]; then
    echo "❌ ADW directory not found at $ADW_DIR"
    exit 1
fi
echo "✓ ADW directory found: $ADW_DIR"

# Check ADW scripts
for script in adw_plan.py adw_build.py adw_test.py adw_plan_build.py adw_plan_build_test.py; do
    if [ -f "$ADW_DIR/$script" ]; then
        echo "✓ $script found"
    else
        echo "❌ $script not found"
        exit 1
    fi
done

echo ""
echo "========================================="
echo "✅ ADW Environment Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Configure .env file with your GitHub and Anthropic API keys"
echo "2. Run a workflow: ./scripts/run_adw.sh <issue-number>"
echo ""
