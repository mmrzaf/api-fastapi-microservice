# FastAPI Microservice Template

A production-ready FastAPI microservice template that is stateless, config-driven, and resource-efficient.

## Features

- ** FastAPI** - Modern, fast web framework for building APIs
- ** Configuration Management** - Environment-based configuration with Pydantic Settings
- ** Monitoring & Metrics** - Built-in Prometheus metrics and health checks
- ** Structured Logging** - JSON logging with correlation IDs
- ** Resource Management** - Proper startup/shutdown lifecycle management
- ** Docker Ready** - Multi-stage Docker builds with security best practices
- ** Testing** - Comprehensive test suite with pytest
- ** Code Quality** - Black, Ruff, and MyPy for code quality and type checking

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip
- Docker (optional)

### Installation

1. **Clone the template:**
   ```bash
   git clone https://github.com/Mohammadreza-Farkhondeh/api-fastapi-microservice
   cd api-fastapi-microservice
````

2.  **Install dependencies:**

    ```bash
    poetry install
    # or with pip
    pip install -r requirements.txt
    ```

3.  **Configure environment:**

    ```bash
    cp .env.example .env
    # Edit .env with your settings
    ```

4.  **Run the application:**

    ```bash
    poetry run uvicorn src.app.main:app --reload
    # or
    python -m uvicorn src.app.main:app --reload
    ```

5.  **Access the application:**

      - API: http://localhost:8000
      - Docs: http://localhost:8000/docs
      - Health: http://localhost:8000/api/v1/health
      - Metrics: http://localhost:8000/api/v1/metrics

### Docker

```bash
# Build the image
docker build -t api-fastapi-microservice .

# Run the container
docker run -p 8000:8000 api-fastapi-microservice
```

## Project Structure

```
api-fastapi-microservice/
├── src/app/
│   ├── api/v1/        # API endpoints
│   ├── core/          # Core functionality
│   └── main.py        # Application entry point
├── tests/             # Test suite
├── Dockerfile         # Container configuration
├── pyproject.toml     # Project dependencies
└── README.md
```

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options.

Key configuration categories:

  - **Application**: Name, version, debug mode
  - **Server**: Host, port, workers
  - **Logging**: Level, format (JSON/console)
  - **API**: Prefixes, CORS settings
  - **Monitoring**: Health check details, metrics

## Development

### Code Quality

```bash
poetry run black src/ tests/

poetry run ruff check src/ tests/

poetry run mypy src/
```

### Testing

```bash
poetry run pytest
poetry run pytest --cov=src --cov-report=html
poetry run pytest tests/unit/test_health.py -v
```

## Monitoring

### Health Checks

  - **Endpoint**: `GET /api/v1/health`
  - **Purpose**: Service health status and system metrics
  - **Configuration**: Set `HEALTH_CHECK_DETAILS=true` for detailed system info

### Metrics

  - **Endpoint**: `GET /api/v1/metrics`
  - **Format**: Prometheus text format
  - **Metrics**:
      - HTTP request counter
      - Request duration histogram
      - Application info

## Deployment

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
APP_NAME="My Microservice"
LOG_LEVEL=INFO
PORT=8000
```

### Production Deployment

1.  **Build production image:**

    ```bash
    docker build --target production -t my-service:latest .
    ```

2.  **Run with proper resource limits:**

    ```bash
    docker run -d \
      --name my-service \
      -p 8000:8000 \
      --memory=512m \
      --cpus=1 \
      -e LOG_LEVEL=INFO \
      my-service:latest
    ```

## Extending the Template

### Adding New Endpoints

1.  Create endpoint in `src/app/api/v1/endpoints/`
2.  Add router to `src/app/api/v1/router.py`
3.  Add tests in `tests/`

### Adding Dependencies

```bash
poetry add <package-name>
poetry add --group dev <dev-package-name>
```

### Custom Middleware

Add middleware in `src/app/main.py`:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.allowed_hosts
)
```

## Security Considerations

  - Non-root user in Docker container
  - No secrets in environment variables (use secret management)
  - Proper CORS configuration
  - Input validation with Pydantic
  - Security headers via middleware

## Contributing

1.  Fork the repository
2.  Create a feature branch
3.  Make your changes
4.  Add tests
5.  Run quality checks
6.  Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
