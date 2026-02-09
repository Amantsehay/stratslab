# Feature: Swagger API Documentation

## Metadata
- **Type**: Feature
- **Status**: Planning
- **Created**: 2026-02-02
- **Updated**: 2026-02-02
- **Agent**: Claude Code

## Feature Description

Enable interactive Swagger (OpenAPI) API documentation for the StratslabAPI, accessible at `http://host:8000/api-docs`. This feature provides developers and API consumers with a comprehensive, interactive interface to explore all available API endpoints, understand request/response schemas, and test endpoints directly through the UI.

The implementation includes:
- Swagger UI (OpenAPI documentation) available at `/api-docs`
- Auto-generated OpenAPI schema from code
- Proper endpoint tagging and organization for better UI presentation
- Request/response examples in documentation
- Authentication documentation for JWT-protected endpoints
- Optional ReDoc alternative documentation at `/redoc`
- Full configuration flexibility through environment variables

## User Story

As a **developer or API consumer**
I want to **access interactive API documentation at `/api-docs`**
So that **I can explore endpoints, understand request/response schemas, test API calls, and integrate with the StratslabAPI more efficiently**

## Problem Statement

Currently, the API documentation is disabled (`docs_url` and `redoc_url` are set to `None` in the FastAPI configuration). This makes it difficult for:
- New developers to discover available endpoints
- API consumers to understand endpoint requirements and response formats
- Testers to manually verify API behavior without writing code
- Teams to maintain up-to-date API documentation

## Solution Statement

Enable Swagger UI documentation by:
1. Configuring FastAPI to serve Swagger UI at the custom path `/api-docs` (instead of default `/docs`)
2. Ensuring OpenAPI schema is properly generated with endpoint documentation
3. Adding comprehensive docstrings and examples to routers
4. Documenting authentication requirements for protected endpoints
5. Configuring UI appearance and behavior for optimal user experience
6. Making documentation URL configurable via environment variables for flexibility

## Acceptance Criteria

1. **Swagger UI Accessibility**
   - Documentation accessible at `http://host:8000/api-docs`
   - UI loads and renders without errors
   - All endpoints are visible in the documentation
   - Tags are properly organized (e.g., "root", "api", "graphql")

2. **Endpoint Documentation**
   - Each endpoint has clear descriptions
   - Request parameters are documented with types and defaults
   - Response schemas are visible with status codes
   - Examples of requests/responses are shown where applicable

3. **Authentication Documentation**
   - JWT authentication is properly documented
   - Protected endpoints are clearly marked
   - Token format and placement in headers is explained

4. **Configuration & Flexibility**
   - Documentation URL can be customized via environment variable
   - ReDoc documentation available as alternative (optional)
   - OpenAPI schema version is configurable
   - Favicon and branding can be customized

5. **No Breaking Changes**
   - Existing API functionality remains unchanged
   - All existing endpoints continue to work
   - No performance degradation from documentation serving
   - Tests continue to pass without modification

## Relevant Files

### Modified Files
- `stratslabapi/apps/fastapi.py` - Configure Swagger UI paths and settings
- `stratslabapi/core/_settings.py` - Add configuration for documentation URLs and OpenAPI settings
- `stratslabapi/routers/__init__.py` - Ensure proper router organization and tagging
- `stratslabapi/routers/health.py` or similar - Add health/root endpoints with documentation (if doesn't exist)

### New Files
- `specs/features/swagger-api-documentation.md` - This feature specification

### Configuration Files
- `.env` and `.env.docker.example` - Add documentation URL configuration variables

## Design Decisions

### Alternatives Considered

1. **Use default FastAPI paths (`/docs` and `/redoc`)**
   - **Rejected**: User specifically requested `/api-docs` as the documentation endpoint
   - Different from defaults but more intuitive for API consumers

2. **Disable documentation entirely (keep current state)**
   - **Rejected**: Contradicts user requirement and best practices for API development
   - Makes API harder to use and discover

3. **Custom documentation implementation**
   - **Rejected**: FastAPI's built-in Swagger UI is mature, well-maintained, and widely understood
   - No need to reinvent the wheel

### Selected Approach

Use FastAPI's native Swagger UI (powered by Swagger UI library) with:
- Custom path configuration at `/api-docs`
- Comprehensive endpoint documentation through docstrings
- Environment variable for configuration flexibility
- ReDoc as alternative documentation view (optional)

### Key Architectural Decisions

- **Documentation as Code**: Use Python docstrings and Pydantic models for documentation (self-documenting)
- **Environment-Driven Configuration**: Make documentation URLs and OpenAPI settings configurable through environment variables
- **Consistent with FastAPI Patterns**: Follow FastAPI conventions for documentation setup
- **Separate Concerns**: Keep documentation configuration in settings and FastAPI app initialization separate
- **Extensibility**: Design to easily add more documentation features (versions, themes, custom styling) in the future

## API Contracts & Data Models

### Documentation Endpoints

```
GET /api-docs              # Swagger UI (main documentation interface)
GET /redoc                 # ReDoc UI (alternative documentation view, optional)
GET /openapi.json          # OpenAPI schema (for consuming documentation programmatically)
```

### OpenAPI Schema Structure

The OpenAPI schema will be auto-generated by FastAPI with:
- API title: "StratslabAPI"
- API description: "AI-powered trading strategy backtesting platform"
- Version: From `__version__.py`
- Servers: Configurable through settings
- Security schemes: JWT bearer token authentication
- Tags: Organized by domain (api, root, graphql)

## Dependencies & Blockers

### External Dependencies
- **fastapi**: Already included, no new version requirements
- **swagger-ui-py**: Bundled with FastAPI, no new installation needed
- No additional Python packages required

### Internal Dependencies
- `stratslabapi.core.settings` - Configuration management
- `stratslabapi.__version__` - Version information
- All existing routers - Will be documented automatically

### Blockers
- None identified. Feature is purely additive and doesn't block other work

## Implementation Plan

### Phase 1: Foundation
- Update settings to include documentation configuration options
- Add environment variables for documentation URL customization
- Review FastAPI documentation setup best practices

### Phase 2: Core Implementation
- Modify FastAPI app initialization to enable Swagger UI at `/api-docs`
- Configure OpenAPI schema generation with proper metadata
- Add comprehensive docstrings to routers
- Document authentication requirements in OpenAPI schema

### Phase 3: Integration & Testing
- Verify documentation loads correctly at `/api-docs`
- Test that all endpoints appear in documentation
- Validate request/response schemas are correct
- Ensure documentation is accessible with and without authentication
- Update README with documentation URL information
- Test in both local and Docker environments

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Prepare Environment and Configuration
- Read existing settings in `stratslabapi/core/_settings.py`
- Add documentation URL configuration variables to Settings class
- Add OpenAPI metadata configuration (title, version, servers)
- Update `.env` and `.env.docker.example` with new documentation variables

### Step 2: Modify FastAPI Application Initialization
- Update `stratslabapi/apps/fastapi.py` to use settings for documentation configuration
- Remove hardcoded `docs_url=None` and `redoc_url=None`
- Configure Swagger UI path to `/api-docs`
- Configure optional ReDoc path to `/redoc`
- Add OpenAPI configuration to FastAPI initialization

### Step 3: Document API Endpoints
- Add comprehensive docstrings to routers (`stratslabapi/routers/__init__.py`)
- Ensure all router endpoints have descriptions and tags
- Add response model documentation where applicable
- Document any required authentication or parameters

### Step 4: Verify Root Endpoints
- Check if health/root endpoints exist in `stratslabapi/routers/__init__.py`
- If not, create basic health endpoint with documentation
- Ensure root endpoints are properly tagged

### Step 5: Testing and Validation
- Start API server locally
- Access Swagger UI at `http://localhost:8000/api-docs`
- Verify documentation loads and displays all endpoints
- Test endpoint documentation accuracy
- Test in Docker environment
- Run all existing tests to ensure no regressions

### Step 6: Documentation Updates
- Update `README.md` with `/api-docs` URL information
- Document how to customize documentation URLs
- Add information about OpenAPI schema access
- Include screenshots or links to documentation in contribution guide

## Testing Strategy

### Unit Tests
- No unit tests required for configuration-only changes
- Settings validation tests for new documentation variables (if any complex logic added)

### Integration Tests
- Test that `/api-docs` endpoint returns HTTP 200
- Test that `/openapi.json` endpoint returns valid OpenAPI schema
- Test that all routers are documented in the schema
- Test documentation with and without authentication headers

### End-to-End Tests
- Start server and verify documentation loads in browser
- Test that Swagger UI displays all endpoints
- Test that endpoint schemas match implementation
- Verify documentation accessibility from Docker environment

### Edge Cases
- Documentation endpoint should not require authentication (publicly accessible)
- Documentation should work with different environment variable configurations
- Documentation should include all dynamic routes from routers
- Performance: Documentation generation should not slow down API startup significantly

## Security & Performance Considerations

### Security
- **Public Accessibility**: Documentation endpoints are intentionally public (information disclosure is expected)
- **Schema Disclosure**: OpenAPI schema reveals endpoint names, parameters, and models (by design)
- **Best Practice**: This is standard for REST APIs; sensitive information should never be in schemas
- **No Sensitive Data**: Ensure no API keys, tokens, or internal implementation details in documentation
- **Authentication Endpoints**: Properly document that authentication endpoints require credentials

### Performance
- **Static Asset Serving**: Swagger UI files are served once and cached by browser
- **Schema Generation**: OpenAPI schema is generated at startup (negligible overhead)
- **Caching**: Browser caches static documentation files
- **No Runtime Impact**: Documentation serving has minimal impact on API performance

## Migration Strategy

Not applicable - this is a new feature addition with no data migration required.

## Rollback Plan

If documentation causes issues:
1. Set `docs_url=None` and `redoc_url=None` in FastAPI initialization
2. Or set `DOCS_URL` environment variable to empty string or `false`
3. This immediately disables documentation without code changes
4. All API functionality remains unaffected

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

### Local Development
```bash
# Start the API server locally
poetry run uvicorn stratslabapi.web_servers.asgi:app --reload --port 8000

# In another terminal, verify documentation is accessible
curl -I http://localhost:8000/api-docs
# Should return HTTP 200

# Verify OpenAPI schema is accessible
curl http://localhost:8000/openapi.json | jq .

# Run all tests to ensure no regressions
poetry run pytest tests/ -v

# Run with specific test categories
poetry run pytest tests/ -v -k "test_" --tb=short
```

### Docker Validation
```bash
# Start containers
./scripts/docker.sh up

# In another terminal, verify documentation in Docker
curl -I http://localhost:8000/api-docs
# Should return HTTP 200

# Verify the documentation loads with a browser
# Open: http://localhost:8000/api-docs

# Stop containers
./scripts/docker.sh down
```

### Browser Testing
- Open `http://localhost:8000/api-docs` in a web browser
- Verify Swagger UI loads without errors
- Check that all routers are visible in the documentation
- Expand endpoints and verify schemas are displayed correctly
- Test endpoint expansion and collapse functionality
- Verify responsive design on different screen sizes

## Notes

- **Customization**: The `/api-docs` path is user-requested; future PRs can add themes or styling via environment variables
- **ReDoc**: Optional ReDoc endpoint at `/redoc` provides an alternative documentation view
- **OpenAPI Schema**: The OpenAPI 3.1.0 schema is served at `/openapi.json` and can be consumed by tools like Postman, Insomnia, etc.
- **Docstring Format**: Use standard Python docstrings in router functions for documentation
- **Future Enhancements**: Consider adding API versioning, webhook documentation, or multi-language support in future iterations
- **Browser Compatibility**: Swagger UI works on all modern browsers (Chrome, Firefox, Safari, Edge)

