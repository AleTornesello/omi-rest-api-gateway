# OMI REST API Gateway

Enterprise Python REST API scaffold for querying the Italian **Osservatorio del Mercato Immobiliare (OMI)** portal through a clean FastAPI interface.

The service is built with:

- Python 3.13
- FastAPI
- uv for dependency management, locking, scripts, and local execution
- Pydantic Settings for typed configuration
- HTTPX for upstream OMI portal calls
- Ruff, mypy, pytest, and coverage for quality gates

> Data source attribution: `Agenzia Entrate - OMI`.

## Project Status

This repository contains the production-ready API scaffold and the boundaries needed to implement the OMI portal integration. The upstream client currently returns an empty result set until the real OMI portal search flow is mapped in `src/omi_rest_api_gateway/clients/omi.py`.

## Architecture

```text
src/omi_rest_api_gateway
├── api/                 # FastAPI routers and versioned endpoints
├── clients/             # Upstream HTTP clients
├── core/                # Settings, logging, exception handlers
├── schemas/             # API request/response models
├── services/            # Business orchestration
├── dependencies.py      # FastAPI dependency providers
└── main.py              # App factory, middleware, lifespan, CLI entry
```

The application uses an app factory (`create_app`) and FastAPI lifespan startup to create shared infrastructure such as the upstream HTTP client.

## API

```http
GET /
GET /api/v1/health/live
GET /api/v1/health/ready
GET /api/v1/omi/quotations
GET /api/v1/openapi.json
GET /docs
```

Example request:

```http
GET /api/v1/omi/quotations?province=MI&municipality=Milano&semester=2025-2&propertyType=abitazioni&contractType=sale
```

Example response:

```json
{
  "source": "Agenzia Entrate - OMI",
  "query": {
    "province": "MI",
    "municipality": "Milano",
    "zone": null,
    "semester": "2025-2",
    "propertyType": "abitazioni",
    "contractType": "sale"
  },
  "results": []
}
```

## Getting Started

Install dependencies:

```bash
uv sync
```

Run the API locally:

```bash
uv run uvicorn omi_rest_api_gateway.main:app --reload --host 0.0.0.0 --port 8080
```

Open:

```text
http://localhost:8080/docs
```

You can also run the packaged entry point:

```bash
uv run omi-rest-api-gateway
```

## Configuration

Copy the example environment file and adjust it for your environment:

```bash
cp .env.example .env
```

Main variables:

```env
OMI_API_ENVIRONMENT=local
OMI_API_HOST=0.0.0.0
OMI_API_PORT=8080
OMI_API_LOG_LEVEL=INFO
OMI_API_API__PREFIX=/api/v1
OMI_API_OMI__BASE_URL=https://www.agenziaentrate.gov.it
OMI_API_OMI__TIMEOUT_SECONDS=30
OMI_API_OMI__CACHE_TTL_SECONDS=86400
```

Nested settings use `__`, for example `OMI_API_API__PREFIX`.

## Development

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Run formatting:

```bash
uv run ruff format .
```

Run type checks:

```bash
uv run mypy src tests
```

Run all local quality gates:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
```

## Docker

Build:

```bash
docker build -t omi-rest-api-gateway .
```

Run:

```bash
docker run --rm -p 8080:8080 --env-file .env omi-rest-api-gateway
```

## CI

GitHub Actions is configured in `.github/workflows/ci.yml` to run:

- dependency sync with uv
- Ruff linting
- Ruff format check
- mypy
- pytest with coverage

## OMI Data Notice

This project is not affiliated with Agenzia delle Entrate.

OMI quotations provide broad market ranges by area, period, and property category. They are useful as a reference, but they are not a formal appraisal and should not replace professional real-estate valuation.

When using OMI data, cite the source as:

```text
Agenzia Entrate - OMI
```

## License

Add the project license here.
