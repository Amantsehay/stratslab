# stratslab

AI-powered trading strategy backtesting platform with distributed services for strategy analysis, AI-driven insights, and performance evaluation.

## Overview

stratslab is a comprehensive backtesting framework that combines machine learning capabilities with quantitative analysis to evaluate and optimize trading strategies. The platform is built as a microservices architecture designed for Kubernetes deployment, enabling scalable strategy analysis and AI-powered decision making.

## Architecture

The project consists of multiple distributed services:

### API Service (`stratslabapi`)
- **FastAPI-based REST API** - Main backend service for strategy management and backtesting requests
- **Authentication & Security** - JWT-based auth with middleware for CORS, request counting, and security headers
- **Database Layer** - SQLAlchemy ORM with repository pattern for data persistence
- **Dependency Injection** - FastAPI's built-in DI system for managing service dependencies

### AI Service (Coming Soon)
- LLM/ML model integration for strategy analysis and optimization recommendations
- Feature engineering and signal processing
- Pattern recognition in historical data

### Backtesting Service (Coming Soon)
- Distributed job-based system for running strategy backtests
- Performance metrics calculation (Sharpe ratio, drawdown, returns, etc.)
- Historical data processing and simulation
- Queue-based job management for scalability

## Project Structure

```
stratslabapi/
├── apps/              # Application initialization (FastAPI setup)
├── core/              # Core configuration (settings, environment)
├── dependencies/      # FastAPI dependency injection (auth, etc.)
├── middlewares/       # HTTP middleware (CORS, security, metrics)
├── repositories/      # Data access layer (models, ORM)
├── routers/           # API endpoints
├── schemas/           # Pydantic request/response models
├── helpers/           # Utility functions (JWT, hashing, validation)
├── utils/             # Compatibility and helper utilities
└── web_servers/       # Web server configuration
```

## Getting Started

### Prerequisites
- Python 3.x (see `.python-version`)
- Poetry for dependency management
- Kubernetes cluster (for production deployment)

### Installation

```bash
# Install dependencies
poetry install

# Copy environment template
cp .env.example .env

# Run the API service
poetry run python -m stratslabapi
```

### Environment Configuration
See `.env.example` for required environment variables (API keys, database URLs, etc.)

## Services Overview

### Development Workflow
- Run API service locally for development and testing
- Services will be containerized and orchestrated with Kubernetes in production

### Deployment
Services are designed to run in Kubernetes:
- **API Service** - REST API container
- **AI Service** - ML/LLM processing service
- **Backtesting Service** - Job-based backtest runner with work queue

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Auth**: JWT
- **Package Manager**: Poetry
- **Deployment**: Kubernetes

## License

See LICENSE file for details.