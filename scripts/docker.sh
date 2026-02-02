#!/bin/bash
# Docker helper script for common operations
# Usage: ./scripts/docker.sh <command>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${GREEN}➜${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Generate a secure random SECRET_KEY
generate_secret_key() {
    python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || \
    openssl rand -base64 32 2>/dev/null || \
    head -c 32 /dev/urandom | base64
}

# Validate .env file for insecure configurations
validate_env_file() {
    local env_file="$1"
    if [ ! -f "$env_file" ]; then
        return 0
    fi
    
    # Check for placeholder SECRET_KEY values
    if grep -q "SECRET_KEY=CHANGE-ME-INSECURE-PLACEHOLDER" "$env_file" 2>/dev/null; then
        print_error "SECURITY WARNING: Your .env file contains an insecure placeholder SECRET_KEY!"
        print_error "Please update SECRET_KEY in .env with a secure random value."
        print_info "Generate a new key with: python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
        exit 1
    fi
    
    # Check for other common insecure placeholders
    if grep -E "SECRET_KEY=.*(your-secret-key-here|change-me|placeholder|example|test|REPLACE|TODO)" "$env_file" 2>/dev/null; then
        print_error "SECURITY WARNING: Your .env file appears to contain a placeholder SECRET_KEY!"
        print_error "Please update SECRET_KEY in .env with a secure random value."
        print_info "Generate a new key with: python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
        exit 1
    fi
}

# Create .env file from template with auto-generated SECRET_KEY
create_env_from_template() {
    local template_file="$PROJECT_ROOT/.env.docker.example"
    local env_file="$PROJECT_ROOT/.env"
    
    if [ ! -f "$template_file" ]; then
        print_error "Template file .env.docker.example not found!"
        exit 1
    fi
    
    print_warning ".env file not found. Creating from .env.docker.example..."
    
    # Generate a secure random SECRET_KEY
    local secret_key=$(generate_secret_key)
    if [ -z "$secret_key" ]; then
        print_error "Failed to generate SECRET_KEY. Please create .env manually."
        exit 1
    fi
    
    # Copy template and replace placeholder SECRET_KEY with generated one
    cp "$template_file" "$env_file"
    
    # Replace the placeholder SECRET_KEY with the generated one
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/SECRET_KEY=CHANGE-ME-INSECURE-PLACEHOLDER/SECRET_KEY=$secret_key/" "$env_file"
    else
        # Linux
        sed -i "s/SECRET_KEY=CHANGE-ME-INSECURE-PLACEHOLDER/SECRET_KEY=$secret_key/" "$env_file"
    fi
    
    print_info "Created .env file with auto-generated SECRET_KEY"
    print_warning "Review and update other settings in .env as needed (database passwords, ports, etc.)"
}

# Check if Docker is running
check_docker() {
    if ! docker ps > /dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker and try again."
        exit 1
    fi
}

# Display help
show_help() {
    cat << EOF
Docker Helper Script for StratslabAPI

Usage: ./scripts/docker.sh <command>

Commands:
    up              Start containers in foreground (see logs directly)
    up-d            Start containers in background (detached mode)
    down            Stop and remove containers
    logs            View combined logs from all services
    logs-api        View logs from API service only
    logs-db         View logs from PostgreSQL service only
    exec-api        Execute command in API container
    exec-db         Execute command in PostgreSQL container
    rebuild         Rebuild images without using cache
    ps              Show container status
    clean           Remove containers, images, and volumes (DESTRUCTIVE)
    help            Show this help message

Environment:
    .env file is required for configuration. Copy from .env.docker.example:
    \$ cp .env.docker.example .env

Examples:
    # Start containers with live logs
    \$ ./scripts/docker.sh up

    # Start containers in background
    \$ ./scripts/docker.sh up-d

    # View API logs
    \$ ./scripts/docker.sh logs-api

    # Run tests in API container
    \$ ./scripts/docker.sh exec-api poetry run pytest tests/

    # Connect to PostgreSQL
    \$ ./scripts/docker.sh exec-db psql -U postgres -d stratslab_dev

EOF
}

# Start containers in foreground
start_foreground() {
    check_docker
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        create_env_from_template
    fi
    validate_env_file "$PROJECT_ROOT/.env"
    print_info "Starting containers in foreground..."
    cd "$PROJECT_ROOT"
    docker-compose up
}

# Start containers in background
start_background() {
    check_docker
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        create_env_from_template
    fi
    validate_env_file "$PROJECT_ROOT/.env"
    print_info "Starting containers in background..."
    cd "$PROJECT_ROOT"
    docker-compose up -d
    print_info "Containers started. Use './scripts/docker.sh logs' to view logs."
}

# Stop containers
stop_containers() {
    check_docker
    print_info "Stopping containers..."
    cd "$PROJECT_ROOT"
    docker-compose down
    print_info "Containers stopped."
}

# Show logs
show_logs() {
    check_docker
    cd "$PROJECT_ROOT"
    print_info "Showing logs from all services (Ctrl+C to exit)..."
    docker-compose logs -f --tail=50
}

# Show API logs
show_api_logs() {
    check_docker
    cd "$PROJECT_ROOT"
    print_info "Showing API logs (Ctrl+C to exit)..."
    docker-compose logs -f --tail=50 api
}

# Show database logs
show_db_logs() {
    check_docker
    cd "$PROJECT_ROOT"
    print_info "Showing PostgreSQL logs (Ctrl+C to exit)..."
    docker-compose logs -f --tail=50 postgres
}

# Execute command in API container
exec_api() {
    check_docker
    if [ $# -eq 0 ]; then
        print_error "Please provide a command to execute in the API container."
        echo "Usage: ./scripts/docker.sh exec-api <command>"
        exit 1
    fi
    cd "$PROJECT_ROOT"
    print_info "Executing in API container: $*"
    docker-compose exec api "$@"
}

# Execute command in database container
exec_db() {
    check_docker
    if [ $# -eq 0 ]; then
        print_error "Please provide a command to execute in the PostgreSQL container."
        echo "Usage: ./scripts/docker.sh exec-db <command>"
        exit 1
    fi
    cd "$PROJECT_ROOT"
    print_info "Executing in PostgreSQL container: $*"
    docker-compose exec postgres "$@"
}

# Rebuild containers
rebuild_images() {
    check_docker
    print_info "Rebuilding containers without cache..."
    cd "$PROJECT_ROOT"
    docker-compose build --no-cache
    print_info "Rebuild complete."
}

# Show container status
show_status() {
    check_docker
    cd "$PROJECT_ROOT"
    print_info "Container status:"
    docker-compose ps
}

# Clean up everything (DESTRUCTIVE)
cleanup() {
    check_docker
    print_warning "This will remove all containers, images, and volumes. This is DESTRUCTIVE!"
    read -p "Are you sure you want to continue? (yes/no) " -r
    echo
    if [[ $REPLY =~ ^[Yy]([Ee][Ss])?$ ]]; then
        print_info "Removing containers..."
        cd "$PROJECT_ROOT"
        docker-compose down -v
        print_info "Cleanup complete."
    else
        print_info "Cleanup cancelled."
    fi
}

# Main command dispatcher
case "${1:-help}" in
    up)
        start_foreground
        ;;
    up-d)
        start_background
        ;;
    down)
        stop_containers
        ;;
    logs)
        show_logs
        ;;
    logs-api)
        show_api_logs
        ;;
    logs-db)
        show_db_logs
        ;;
    exec-api)
        shift
        exec_api "$@"
        ;;
    exec-db)
        shift
        exec_db "$@"
        ;;
    rebuild)
        rebuild_images
        ;;
    ps)
        show_status
        ;;
    clean)
        cleanup
        ;;
    help)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
