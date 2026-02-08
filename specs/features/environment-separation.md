# Feature: Multi-Environment Configuration Management

## Metadata
- **Type**: Feature
- **Status**: Planning
- **Created**: 2026-02-02
- **Updated**: 2026-02-02
- **Agent**: Claude Haiku 4.5

## Feature Description

This feature introduces a structured environment management system that separates application configuration into three distinct environments: **development**, **local**, and **production**. Currently, the application uses a single `.env` file with fallback values, making it difficult to maintain different configurations for different deployment contexts.

The new system will:
- Create environment-specific `.env` files (`.env.local`, `.env.development`, `.env.production`)
- Add an `APP_ENV` variable that controls which configuration is loaded
- Make `.env` files the single source of truth for all environment-specific settings
- Update Docker Compose to read `APP_ENV` from the `.env` file
- Maintain backward compatibility with existing deployments
- Simplify local development, CI/CD pipeline setup, and production deployment

## User Story

As a **developer/DevOps engineer**, I want to **manage separate configuration files for different environments**, so that **I can easily switch between local development, testing, and production setups without accidentally deploying development settings to production**.

## Problem Statement

Currently, the application's environment configuration has several pain points:

1. **Single `.env` file for all purposes**: There's no clear separation between local development and production configurations
2. **Unclear defaults**: The `docker-compose.yml` has fallback values (e.g., `${POSTGRES_DB:-stratslab_dev}`) that may not match the intended production defaults
3. **Risk of configuration mismatches**: Developers might use local settings and accidentally commit them, or production deployments might use incorrect configurations
4. **Difficult to manage multiple deployments**: Teams running multiple instances (staging, production) need different configurations but have no clean way to manage them
5. **Lack of APP_ENV as source of truth**: The environment is inferred from file presence rather than explicitly declared

## Solution Statement

Implement a formal environment management system with:

1. **Three environment-specific configuration files**:
   - `.env.development`: For development environment (with hot-reload, debug logging, local defaults)
   - `.env.local`: For local machine testing (like development but isolated)
   - `.env.production`: For production deployments (minimal logging, secure defaults, optimized settings)

2. **APP_ENV variable as source of truth**:
   - The `.env` file (which is not committed to git) will contain `APP_ENV=development|local|production`
   - The application will load the corresponding `.env.<APP_ENV>` file
   - This ensures configuration is explicitly declared and prevents confusion

3. **Updated settings system**:
   - Modify `stratslabapi/core/_settings.py` to support environment-specific loading
   - Implement proper precedence: `APP_ENV` → environment-specific file → defaults

4. **Docker Compose integration**:
   - Update `docker-compose.yml` to read `APP_ENV` from the `.env` file
   - Use `APP_ENV` to determine which settings to apply
   - Maintain support for `.env.docker.example` for Docker users

5. **Documentation and examples**:
   - Create `.env.example` that shows the basic structure with `APP_ENV`
   - Update README.md with environment setup instructions
   - Document best practices for each environment

## Acceptance Criteria

1. ✅ Three environment files exist: `.env.development`, `.env.local`, `.env.production` (committed to repo)
2. ✅ `.env` file contains `APP_ENV` variable (not committed, created from example)
3. ✅ Settings system loads correct file based on `APP_ENV` value
4. ✅ Docker Compose reads `APP_ENV` from `.env` and applies correct configuration
5. ✅ `.env.example` demonstrates the structure with `APP_ENV=development` as default
6. ✅ `.env.docker.example` works as before and sets `APP_ENV=development`
7. ✅ Running locally uses `.env.local` when `APP_ENV=local`
8. ✅ All existing tests pass with zero regressions
9. ✅ README.md updated with environment setup instructions
10. ✅ `.gitignore` updated to exclude only `.env` (not `*.env` files)
11. ✅ Developers can switch environments by changing `APP_ENV` in `.env`
12. ✅ Docker deployments work for all three environments

## Relevant Files

Use these files to implement the feature:

- `stratslabapi/core/_settings.py` - Core settings loader (primary change)
- `docker-compose.yml` - Docker Compose configuration
- `.env.example` - Base environment file template
- `.env.docker.example` - Docker-specific environment template
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation

### New Files to Create

- `.env.development` - Development environment configuration (committed)
- `.env.local` - Local testing environment configuration (committed)
- `.env.production` - Production environment configuration (committed)
- `specs/features/environment-separation.md` - This feature specification

## Design Decisions

### Alternatives Considered

1. **Single `.env` with environment detection** (Rejected)
   - Detection via hostname, Docker labels, or environment variables
   - Problem: Implicit configuration is error-prone and hard to debug

2. **Only local and production** (Rejected)
   - Problem: Developers need a clear dev environment that differs from local testing
   - Local is often used for isolated testing before committing

3. **Load from `.env.${APP_ENV}` without a base `.env`** (Rejected)
   - Problem: Requires every deployment to set `APP_ENV` environment variable first
   - Current setup uses `.env` files as configuration source

4. **Dotenv file hierarchy without APP_ENV** (Rejected)
   - Problem: Unclear which file is loaded and why; requires implicit knowledge

### Selected Approach

Use explicit `APP_ENV` variable as the source of truth:
- The `.env` file (not committed) contains `APP_ENV` declaration
- The settings loader reads `APP_ENV` and loads the corresponding `.env.<APP_ENV>` file
- Three committed environment files (development, local, production) provide templates
- This approach is explicit, maintainable, and easy to debug

### Key Architectural Decisions

1. **APP_ENV is mandatory**: The settings system will fail-fast if `APP_ENV` is not set, preventing accidental misconfigurations
2. **Three environments are intentional**: Development (with debug features), local (isolated testing), and production (secure defaults)
3. **Cascading defaults**: If a variable is not in the environment-specific file, use defaults from `_settings.py`
4. **Docker-compatible**: The system works seamlessly with both local Docker and production Kubernetes deployments
5. **Backward compatibility**: Existing deployments without `APP_ENV` will default to `development` mode (with a warning)

## API Contracts & Data Models

No new API endpoints or data models are required. This feature only affects configuration loading.

### Settings Enhancement

The `Settings` class will gain:
- `app_env: str` field with validation for "development", "local", or "production"
- `load_environment()` class method to load the correct `.env.<APP_ENV>` file
- Enhanced error messages indicating which environment file was loaded

```python
class Settings(BaseSettings):
    # ... existing fields ...
    app_env: str = Field(default="development", description="Application environment")

    @classmethod
    def load_environment(cls) -> "Settings":
        """Load settings based on APP_ENV variable"""
        # Read APP_ENV from environment or .env file
        # Load corresponding .env.<APP_ENV> file
        # Return configured Settings instance
```

## Dependencies & Blockers

- **External Dependencies**: None (using existing pydantic-settings)
- **Internal Dependencies**: None (standalone feature)
- **Blockers**: None identified

## Implementation Plan

### Phase 1: Foundation - Environment File Structure
Create the three environment-specific configuration files with appropriate defaults for each environment type. Ensure they're properly documented and included in version control.

### Phase 2: Core Implementation - Settings System
Enhance the `Settings` class to support loading the correct environment file based on `APP_ENV`. Implement validation and error handling. Update the Docker Compose configuration to respect `APP_ENV`.

### Phase 3: Integration & Documentation
Update all documentation, examples, and deployment scripts. Update `.gitignore` to properly include environment-specific files. Create migration guidance for existing deployments. Add tests to verify correct environment loading.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Environment-Specific Configuration Files

1. Create `.env.development` with development defaults:
   - Database: local development database
   - Debug logging enabled
   - Hot-reload enabled
   - HTTPS redirect disabled
   - Email sending disabled
   - Auto-activate users enabled for testing

2. Create `.env.local` with local testing defaults:
   - Similar to development but with isolated database
   - Minimal logging for testing
   - All flags disabled except what's needed for local testing

3. Create `.env.production` with production-secure defaults:
   - Secure database connection (TLS preferred)
   - Minimal logging (errors only)
   - All debug features disabled
   - HTTPS redirect enabled
   - Email sending enabled
   - Enhanced pool settings for production traffic

4. Update `.env.example` to include `APP_ENV=development` as the first variable
   - Remove development-specific defaults
   - Make it a template that developers copy to `.env`

5. Update `.env.docker.example` to include `APP_ENV=development`
   - Ensure Docker users get development defaults

### Step 2: Enhance Settings System

1. Add `app_env` field to `Settings` class:
   - Type: `str` with validation for ["development", "local", "production"]
   - Default: "development" (with deprecation notice if not explicitly set)

2. Create `load_dotenv_for_environment()` method:
   - Reads `APP_ENV` from environment variables or existing `.env` file
   - Loads the corresponding `.env.<APP_ENV>` file using `dotenv.load_dotenv()`
   - Handles missing files gracefully with informative errors

3. Update `settings_customise_sources()`:
   - Call environment loading before other sources
   - Ensure `.env.<APP_ENV>` values override defaults

4. Add logging to indicate which environment was loaded:
   - Log at startup: "Loaded configuration from .env.development"
   - Log at startup if `APP_ENV` not explicitly set: "APP_ENV not set, using default: development"

5. Update `Settings` instantiation in `_settings.py`:
   - Call environment loading before creating Settings instance
   - Validate that loaded environment is correct

### Step 3: Update Docker Configuration

1. Modify `docker-compose.yml`:
   - Ensure API service reads `APP_ENV` from the `.env` file
   - Pass `APP_ENV` to container environment
   - Verify all environment variables are passed correctly

2. Test Docker Compose:
   - Test with `APP_ENV=development` in `.env`
   - Test with `APP_ENV=production` in `.env`
   - Verify correct settings are loaded in each case

### Step 4: Update Git Configuration

1. Update `.gitignore`:
   - Ensure `.env` is ignored (single file, not `.env*`)
   - Ensure `.env.development`, `.env.local`, `.env.production` are NOT ignored
   - Verify test environment files are properly handled

2. Remove `.env` from git if previously committed:
   - Use `git rm --cached .env` if needed
   - Commit the removal

### Step 5: Update Documentation

1. Update `README.md`:
   - Add section explaining the three environments
   - Document which environment to use for local development
   - Document Docker setup with APP_ENV
   - Document production deployment setup

2. Create inline documentation:
   - Add docstring to `Settings` class explaining environment loading
   - Add comments in environment files explaining each setting

3. Create `.env.example` from `.env.development`:
   - Rename to `.env.example` or copy content
   - Ensure it's the template developers should copy

### Step 6: Add Tests

1. Add unit tests for environment loading:
   - Test loading `.env.development`
   - Test loading `.env.local`
   - Test loading `.env.production`
   - Test invalid APP_ENV value
   - Test missing APP_ENV (should use default)

2. Add integration tests:
   - Test that Docker Compose loads correct environment
   - Test that settings reflect the correct environment
   - Test that switching APP_ENV changes loaded settings

3. Ensure all existing tests still pass:
   - Run full test suite
   - Verify no regressions

### Step 7: Validation and Cleanup

1. Clean up old `.env` files:
   - Back up existing `.env` if it contains custom configurations
   - Create new `.env` from `.env.example` with `APP_ENV=development`

2. Validate setup:
   - Start application with `.env.development`
   - Start application with `.env.production`
   - Verify settings are correctly loaded

3. Document migration path:
   - For existing deployments, guide users to set `APP_ENV` in their `.env`
   - Provide backwards compatibility note

## Testing Strategy

### Unit Tests

Create `tests/test_settings_environment.py`:

```python
def test_load_development_environment():
    """Test loading development environment settings"""
    # Set APP_ENV=development
    # Load settings
    # Verify development-specific settings are applied

def test_load_local_environment():
    """Test loading local environment settings"""
    # Set APP_ENV=local
    # Load settings
    # Verify local-specific settings are applied

def test_load_production_environment():
    """Test loading production environment settings"""
    # Set APP_ENV=production
    # Load settings
    # Verify production-specific settings are applied

def test_invalid_app_env():
    """Test that invalid APP_ENV raises error"""
    # Set APP_ENV=invalid
    # Verify SettingsError is raised

def test_missing_env_file():
    """Test graceful handling of missing environment file"""
    # Ensure .env.development exists but .env.nonexistent doesn't
    # Set APP_ENV=nonexistent
    # Verify informative error message

def test_app_env_default():
    """Test that default APP_ENV is 'development'"""
    # Don't set APP_ENV
    # Verify it defaults to development
```

### Integration Tests

Create `tests/test_docker_environment.py`:

```python
def test_docker_compose_development():
    """Test Docker Compose with development environment"""
    # Start docker-compose with APP_ENV=development
    # Verify API container loads development settings
    # Check logs for "Loaded configuration from .env.development"

def test_docker_compose_production():
    """Test Docker Compose with production environment"""
    # Start docker-compose with APP_ENV=production
    # Verify API container loads production settings
    # Check logs for "Loaded configuration from .env.production"

def test_app_env_from_dotenv():
    """Test that APP_ENV is read from .env file"""
    # Create .env with APP_ENV=local
    # Load settings
    # Verify local environment is loaded
```

### Edge Cases

- APP_ENV is set to an empty string (should use default with warning)
- APP_ENV is set to mixed case "Development" (should normalize and work)
- Environment file has syntax errors (should provide helpful error message)
- Environment file is missing (should fail with clear message indicating which file)
- All three environment files are missing (should fail with clear message)
- APP_ENV contains special characters (should validate and reject)

## Security & Performance Considerations

### Security

1. **Production settings are secure by default**:
   - `.env.production` disables debug features
   - HTTPS redirect is enabled
   - Email sending and user activation are disabled
   - Pool settings are optimized for production traffic

2. **Secret management**:
   - `SECRET_KEY` should be different in each environment
   - Template files don't contain real secrets
   - Production deployment must set real `SECRET_KEY`
   - Documentation guides users to generate strong keys

3. **Environment verification**:
   - Log the loaded environment at startup
   - Fail loudly if `APP_ENV` is invalid
   - Prevent accidental production-setting misconfigurations

### Performance

1. **Settings loading is cached**:
   - Settings are loaded once at application startup
   - No runtime performance impact
   - Using `cached_property` for Fernet key generation

2. **No additional dependencies**:
   - Uses existing `pydantic-settings` library
   - No new external packages needed

3. **Database connection pooling**:
   - Production environment has tuned pool settings
   - Development environment uses minimal pooling
   - Each environment optimized for its use case

## Migration Strategy

### For Existing Deployments

1. **Backward Compatibility Mode**:
   - If `.env` exists but `APP_ENV` is not set, default to `development`
   - Log a warning: "APP_ENV not explicitly set, using default: development. Please set APP_ENV in your .env file."

2. **For Current Users**:
   - Existing `.env` files will continue to work
   - Add `APP_ENV=development` to their existing `.env` file
   - Gradually migrate to new environment-specific files

3. **Docker Users**:
   - `.env.docker.example` includes `APP_ENV=development`
   - Existing `docker-compose` users update their `.env` with `APP_ENV`
   - No breaking changes

### Data Migration

No data migration needed - this is a configuration-only change.

## Rollback Plan

If issues occur:

1. **Rollback configuration loading**:
   - Revert changes to `stratslabapi/core/_settings.py`
   - Application will fall back to default settings

2. **Restore old `.env` files**:
   - Keep backup of original `.env` files
   - Copy original files back
   - Restart application

3. **No data loss**:
   - Database is unaffected by configuration changes
   - All data remains intact

4. **Git rollback** (if committed):
   - `git revert` the commit that introduced the changes
   - Or `git reset --hard` to previous known-good commit

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

```bash
# Run all tests to ensure no regressions
poetry run pytest tests/ -v

# Test environment loading with development
APP_ENV=development poetry run python -c "from stratslabapi.core._settings import settings; print(f'Loaded: {settings.app_env}')"

# Test environment loading with local
APP_ENV=local poetry run python -c "from stratslabapi.core._settings import settings; print(f'Loaded: {settings.app_env}')"

# Test environment loading with production
APP_ENV=production poetry run python -c "from stratslabapi.core._settings import settings; print(f'Loaded: {settings.app_env}')"

# Test Docker Compose with development environment
APP_ENV=development docker-compose config | grep -A 5 "environment:"

# Verify .env files are tracked in git
git ls-files | grep "\.env\."

# Verify .env is not tracked
git status | grep ".env" || echo ".env correctly ignored"

# Start Docker Compose and verify settings
./scripts/docker.sh up-d
sleep 5
./scripts/docker.sh logs-api | grep -i "environment\|loaded"
./scripts/docker.sh down
```

## Notes

### Future Enhancements

1. **Environment-specific logging configurations**:
   - Production: JSON structured logging
   - Development: Colorized console logging

2. **Health check endpoints**:
   - Endpoint to verify which environment is loaded
   - Useful for debugging in containerized environments

3. **Configuration validation**:
   - Add schema validation for each environment
   - Ensure required settings are present before startup

4. **Environment-specific secrets**:
   - Integration with HashiCorp Vault or AWS Secrets Manager
   - Per-environment secret management

### Dependencies Added

No new Python packages needed - uses existing `pydantic-settings` and `python-dotenv`.

### Files Modified

- `stratslabapi/core/_settings.py` - Enhanced to support environment-based loading
- `docker-compose.yml` - Updated to respect APP_ENV
- `README.md` - Added environment documentation
- `.gitignore` - Updated to include but not ignore environment files

### Files Created

- `.env.development` - Development environment configuration
- `.env.local` - Local testing environment configuration
- `.env.production` - Production environment configuration
- Updated `.env.example` - Template for new deployments

### Testing Requirements

- All existing tests must pass
- New test coverage for environment loading (minimum 90%)
- Integration tests for Docker Compose environments
- Manual testing of each environment type

