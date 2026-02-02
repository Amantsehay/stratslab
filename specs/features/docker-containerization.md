# Feature: Docker Containerization Setup

## Metadata
- **Type**: Feature
- **Status**: Planning
- **Created**: 2026-02-02
- **Updated**: 2026-02-02
- **Agent**: Claude Code

## Feature Description

Implement a production-ready Docker containerization setup for the StratslabAPI project with multi-container orchestration using Docker Compose. This feature establishes the foundational infrastructure for running the application and PostgreSQL database in isolated containers, enabling local development, CI/CD integration, and easy deployment. The setup is designed with extensibility in mind to easily accommodate additional services (AI service, backtesting service) in the future.

The containerization includes:
- Custom Dockerfile for FastAPI application with multi-stage build
- Docker Compose configuration for local development
- PostgreSQL container with initialization and persistence
- Health checks for all services
- Volume management for development and database persistence
- Environment configuration for different deployment contexts
- Support for easy service addition without restructuring

## User Story

As a **developer**
I want to **run the entire application stack in Docker containers**
So that **I can have consistent development environments, simplify local setup, and prepare the project for cloud deployment**

## Problem Statement

Currently, developers must manually install PostgreSQL, configure databases, and manage environment variables. This creates inconsistencies across development machines, complicates onboarding, and makes it difficult to test the exact deployment conditions locally. There's no clear path for adding future services (AI, backtesting) without restructuring the infrastructure.

## Solution Statement

Implement Docker and Docker Compose to containerize both the FastAPI application and PostgreSQL database. Create a scalable, extensible infrastructure that:
- Eliminates "works on my machine" problems through containerization
- Simplifies local development with single `docker-compose up` command
- Provides a blueprint for adding microservices without major restructuring
- Enables consistent testing across development, staging, and production environments
- Supports volume management for code changes and database persistence

## Acceptance Criteria

1. **Docker Image Creation**
   - Dockerfile builds a minimal, production-ready image for the API
   - Multi-stage build separates dependency installation from runtime
   - Image size is optimized (< 200MB)
   - Non-root user for security

2. **Docker Compose Setup**
   - Services defined: `api` and `postgres`
   - All services can be started with single command: `docker-compose up`
   - Services are networked and can communicate via container names
   - Development volumes enable code hot-reload

3. **Database Service**
   - PostgreSQL 15+ runs in container with persistence
   - Database initializes on first run
   - Health check ensures readiness before API starts
   - Migrations run automatically on startup

4. **API Service**
   - FastAPI application runs in container
   - Environment variables properly injected from compose file
   - Health endpoint `/health` available and checked
   - Depends on PostgreSQL being healthy before starting

5. **Development Workflow**
   - Code changes reflect immediately in running container (hot-reload)
   - Logs accessible via `docker-compose logs`
   - Easy access to API at `http://localhost:8000`
   - Swagger docs at `http://localhost:8000/docs`

6. **Extensibility**
   - Structure supports adding new services (ai-service, backtesting-service) easily
   - All services can use same compose network
   - Each service has isolated environment configuration
   - Clear patterns for service dependencies

7. **Documentation & Scripts**
   - Update README with Docker setup instructions
   - Provide docker-compose commands reference
   - Create helper script for common Docker operations
   - Clear guidance on local vs. containerized development

## Relevant Files

- `Dockerfile` - Multi-stage Docker image for FastAPI application
- `docker-compose.yml` - Container orchestration for development environment
- `.dockerignore` - Exclude unnecessary files from Docker build context
- `README.md` - Update with containerization instructions
- `scripts/docker-compose.sh` - Helper script for Docker operations
- `.env.docker.example` - Docker-specific environment variables template

### Modified Files
- `pyproject.toml` - May need to add development dependencies if needed
- `.gitignore` - Ensure Docker-related files are handled appropriately

## Design Decisions

### Alternatives Considered

1. **Single Monolithic Dockerfile vs. Multi-stage Build**
   - Considered: Simple, single-stage Dockerfile
   - Rejected: Results in larger image with build dependencies included
   - Selected: Multi-stage build separates build stage from runtime, reducing final image size

2. **Docker Compose Versions**
   - Considered: Using older `docker-compose` v2.x syntax (deprecated)
   - Selected: Using modern `docker-compose` v3.9+ syntax for better compatibility

3. **Database Initialization**
   - Considered: Manual migration on startup
   - Selected: Auto-running migrations in entrypoint script for zero-touch startup

4. **Service Architecture**
   - Considered: One monolithic compose file for all services
   - Selected: Modular structure with ability to scale; future services can be added as separate containers

5. **Volume Management**
   - Considered: No volumes for database (ephemeral)
   - Selected: Named volume for database persistence; bind mount for code hot-reload

### Selected Approach

**Multi-container Docker Compose setup** with:
- Modern `docker-compose.yml` v3.9 syntax
- Python 3.12 slim base image for minimal footprint
- Multi-stage build (build stage + runtime stage)
- Named volume for PostgreSQL persistence
- Bind mount for FastAPI code (development)
- Health checks with retries and timeouts
- Automatic migration execution on startup
- Clear separation of concerns for future microservices

### Key Architectural Decisions

1. **Base Image**: Use `python:3.12-slim` for minimal production footprint while maintaining compatibility
2. **Non-root User**: Create `appuser` for security; run application with reduced privileges
3. **Health Checks**: Implement health checks for both services with 5-second intervals, 30-second timeouts
4. **Service Dependencies**: API explicitly waits for PostgreSQL health before starting
5. **Environment Isolation**: Separate environment files for Docker to keep configs organized
6. **Extensibility Pattern**: Services use standardized naming convention (service-name) for easy addition
7. **Development vs. Production**: Same Dockerfile serves both with different base configurations

## API Contracts & Data Models

No new API endpoints or data models. This feature is purely infrastructure.

## Dependencies & Blockers

### External Dependencies
- Docker Engine 20.10+ (or Docker Desktop)
- Docker Compose 2.0+ (included in Docker Desktop)
- PostgreSQL 15+ (runs in container, no local installation needed)

### Internal Dependencies
- `stratslabapi` module must be importable (existing code)
- Database models must exist (`stratslabapi/repositories/`)
- ASGI application must be created (`stratslabapi/web_servers/asgi.py`)

### Blockers
- ASGI application (`stratslabapi/web_servers/asgi.py`) must be implemented before testing containerized app

## Implementation Plan

### Phase 1: Foundation
Set up Docker configuration files and prepare application for containerization:
- Create `.dockerignore` to exclude build-time unnecessary files
- Create `Dockerfile` with multi-stage build and security best practices
- Create `docker-compose.yml` with api and postgres services
- Create `.env.docker.example` with Docker-specific defaults
- Update `.gitignore` if needed

### Phase 2: Core Implementation
Implement the containerized services with proper configuration:
- Configure PostgreSQL service in compose with volumes and health checks
- Configure API service with depends_on, environment, and volumes
- Create startup script for automatic migrations
- Implement health check endpoint (may already exist)
- Test local container builds and communication

### Phase 3: Integration & Testing
Ensure containers work correctly in development workflow:
- Update README with Docker setup instructions
- Create docker helper script for common commands
- Test full development workflow: start, code changes, logs, cleanup
- Verify hot-reload works for code changes
- Test database persistence across restarts
- Verify health checks work correctly

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Docker Configuration Files
- Create `.dockerignore` with patterns for excluded files (tests, __pycache__, .git, etc.)
- Create `Dockerfile` with:
  - Stage 1 (builder): Python 3.12-slim, install Poetry and dependencies
  - Stage 2 (runtime): Python 3.12-slim, copy app files, create non-root user, set entrypoint
- Create `docker-compose.yml` v3.9 with api and postgres services
- Create `.env.docker.example` with production-ready defaults (secrets must be changed)

### Step 2: Configure Database Service
- Define PostgreSQL 15 service in compose:
  - Image: `postgres:15-alpine`
  - Volumes: named volume `postgres_data` for persistence
  - Environment: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
  - Health check: pg_isready command with retries
  - Ports: 5432 (mapped for development access)

### Step 3: Configure API Service
- Define FastAPI service in compose:
  - Build from `./Dockerfile`
  - Depends on PostgreSQL (wait for health)
  - Environment variables from `.env` file
  - Volumes: bind mount for code, for hot-reload
  - Ports: 8000 (API), optionally 8080 for metrics
  - Health check: HTTP GET to `/health` endpoint
  - Command: uvicorn startup with reload

### Step 4: Create Startup & Migration Scripts
- Create `docker-entrypoint.sh` script that:
  - Runs Alembic migrations (`alembic upgrade head`)
  - Starts uvicorn server with reload enabled for development
- Make script executable
- Reference script in Dockerfile ENTRYPOINT

### Step 5: Update Application Configuration
- Verify environment variable handling in `stratslabapi/core/_settings.py`
- Ensure DATABASE_URL works with Docker networking (use service name as hostname)
- Update example env file with Docker container hostnames

### Step 6: Create Helper Scripts
- Create `scripts/docker.sh` with commands:
  - `up`: Start containers (foreground for logs)
  - `up-d`: Start containers in background
  - `down`: Stop and remove containers
  - `logs`: View combined logs
  - `logs-api`: View API logs only
  - `logs-db`: View database logs only
  - `exec-api`: Execute command in API container
  - `rebuild`: Rebuild images without cache
  - `clean`: Remove images, volumes, containers

### Step 7: Update Documentation
- Update `README.md`:
  - Add "Using Docker" section
  - Document `docker-compose up` command
  - Explain volume management
  - Show how to access Swagger docs in container
  - Document environment variables for Docker
  - Provide troubleshooting tips
- Add example of extending with new services

### Step 8: Create Validation Tests
- Test that Docker image builds successfully
- Test that containers start without errors
- Test that API is accessible at localhost:8000
- Test that database migrations run automatically
- Test that code changes trigger hot-reload
- Test service-to-service communication via compose network
- Test health checks respond correctly
- Test database persistence across restarts

## Testing Strategy

### Unit Tests
- No new unit tests required; feature is infrastructure-based
- Existing pytest tests should pass in containerized environment

### Integration Tests
- **Docker Compose Startup**: Verify all services start without errors
  - API service healthy after startup
  - PostgreSQL accepting connections
  - Services can communicate via compose network

- **Database Connection**: Verify API can connect to containerized PostgreSQL
  - Connection string uses service name (postgres) as hostname
  - Database exists and is ready
  - Tables created by migrations

- **Health Checks**: Verify health check endpoints
  - `/health` endpoint responds with 200 OK
  - PostgreSQL health check uses pg_isready

- **Volume Persistence**: Verify data persists across restarts
  - Create test data in running container
  - Stop and restart containers
  - Verify test data still exists

### End-to-End Tests
- **Local Development Workflow**: Full cycle from code change to API response
  - Start containers with `docker-compose up`
  - Make API request to verify functionality
  - Modify code in host machine
  - Verify hot-reload updates running container
  - Stop containers with `docker-compose down`

- **Service Communication**: Verify multi-service interaction
  - API queries database successfully
  - Connection pooling works correctly
  - Transactions are properly handled

### Edge Cases
- **Container Restart**: API and PostgreSQL restart in any order
- **Network Issues**: Temporary network disconnection and recovery
- **Volume Initialization**: First-time startup with empty volume
- **Environment Variables**: Missing or invalid environment variables handled gracefully
- **Port Conflicts**: Clear error messages if ports already in use

## Security & Performance Considerations

### Security
- **Non-root User**: Application runs as `appuser` with minimal privileges
- **Secret Management**: `.env.docker.example` documents required secrets; actual `.env` is `.gitignore`d
- **Image Scanning**: Recommend using `docker scan` to check for vulnerabilities
- **Network Isolation**: Services only accessible via docker network or mapped ports
- **Read-only Filesystem**: Consider read-only root filesystem for production (future)

### Performance
- **Image Size**: Multi-stage build keeps final image < 200MB (slim base + only runtime dependencies)
- **Layer Caching**: Dockerfile structure optimizes layer caching (dependencies before code)
- **Development Hot-reload**: Bind mount avoids image rebuild for code changes
- **Database Performance**: PostgreSQL alpine image optimized for small container size
- **Connection Pooling**: Existing SQLAlchemy pool settings work in containerized environment

## Migration Strategy

This is a new feature; no data migration required. However:
- Existing local PostgreSQL databases are not affected
- Developers can run both local and containerized versions simultaneously (different ports)
- Clear documentation guides migration from local to containerized development

## Rollback Plan

If containerization causes issues:
1. Developers can revert to local PostgreSQL installation
2. Continue using `poetry run uvicorn` directly without containers
3. Docker Compose configuration can be disabled without affecting application code
4. No database schema changes required for this feature

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

```bash
# Build Docker image without cache
docker-compose build --no-cache

# Start services and check they're running
docker-compose up -d
sleep 5

# Verify API is accessible and healthy
curl -s http://localhost:8000/health | grep -q '"status":"ok"' && echo "✓ API health check passed"

# Verify PostgreSQL is running and accessible
docker-compose exec postgres pg_isready && echo "✓ PostgreSQL ready"

# Run migrations in container (should already have run)
docker-compose exec api alembic current && echo "✓ Database migrations verified"

# Run existing test suite in container
docker-compose exec api poetry run pytest tests/ -v && echo "✓ All tests passed in container"

# Verify hot-reload works (make small change, API reflects it immediately)
# [Manual test: edit a Python file and verify changes appear without container restart]

# Check container logs for errors
docker-compose logs --tail=50 api
docker-compose logs --tail=50 postgres

# Test service communication (API -> PostgreSQL)
docker-compose exec api curl -s http://localhost:8000/docs && echo "✓ Swagger docs accessible"

# Clean up
docker-compose down -v
```

### Additional Validation Steps
1. **Image Build**: `docker build -t stratslab-api:test .` should complete without errors
2. **Compose Validation**: `docker-compose config` should output valid YAML
3. **Health Checks**: `docker-compose ps` should show healthy status for all services
4. **Volume Verification**: `docker volume ls | grep postgres_data` should exist after first run
5. **Network Test**: `docker network inspect stratslab_default` should show both services connected

## Notes

### Future Service Addition Pattern

When adding new services (e.g., AI service, backtesting service), follow this pattern:

```yaml
# In docker-compose.yml
ai-service:
  build:
    context: ./ai-service
    dockerfile: Dockerfile
  environment:
    - DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/stratslab_dev
    - REDIS_URL=redis://redis:6379
  depends_on:
    postgres:
      condition: service_healthy
  volumes:
    - ./ai-service:/app/ai-service
  networks:
    - default
```

### Important Implementation Notes

1. **ASGI Application Dependency**: The feature plan assumes `stratslabapi/web_servers/asgi.py` will be implemented before full testing
2. **Environment Variable Naming**: Use clear conventions: `POSTGRES_HOST` is service name in Docker, `localhost` locally
3. **Database URL Format**: In Docker, use `postgresql+asyncpg://user:pass@postgres:5432/db` (note: service name instead of localhost)
4. **Port Mapping**: Local port:container port; `8000:8000` means localhost:8000 reaches container:8000
5. **Volume Management**:
   - Named volumes (`postgres_data`) persist data but are managed by Docker
   - Bind mounts (`./stratslabapi:/app/stratslabapi`) for code changes in development
6. **Health Checks**: Crucial for proper service startup order; always include for stateful services

### Recommended Enhancements (Future)

1. **Multi-stage Compose Files**: Separate `docker-compose.yml` for dev, staging, production
2. **Kubernetes Manifests**: Add k8s YAML files for cloud deployment
3. **CI/CD Integration**: GitHub Actions workflow that builds and pushes images
4. **Docker Registry**: Push images to private Docker registry (ECR, GCR, etc.)
5. **Secrets Management**: Use Docker Secrets or external vault for sensitive data
6. **Resource Limits**: Add CPU/memory limits to services as they're defined
7. **Logging**: Consider centralized logging (ELK stack, Datadog) for production

### Testing Notes

- Ensure `pytest` dependencies are in `pyproject.toml`
- Health endpoint (`/health`) may need to be implemented if not already present
- Database tests can run against containerized PostgreSQL without modification
- Mock external dependencies in tests rather than containerizing them all
