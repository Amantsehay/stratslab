# Install & Prime

## Read and Execute
.claude/commands/prime.md

## Run
1. Install project dependencies:
```bash
poetry install
```

2. Setup environment:
```bash
./scripts/copy_dot_env.sh
```

3. Verify installation:
```bash
poetry run python -c "import stratslabapi; print('✓ Import successful')"
```

## Report
Output the work you've just done in a concise bullet point list:
- Dependencies installed with poetry
- Environment file configured
- Development environment ready