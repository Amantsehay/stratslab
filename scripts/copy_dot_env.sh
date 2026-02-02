#!/bin/bash
# Copy environment template if .env doesn't exist
# Sets up the .env file from .env.example for development

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env from .env.example"
    else
        echo "Error: .env.example not found"
        exit 1
    fi
else
    echo "✓ .env already exists"
fi
