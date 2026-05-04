# OMI REST API Gateway

REST API service for querying the Italian OMI portal through a simple HTTP interface.

The project exposes data from the **Osservatorio del Mercato Immobiliare (OMI)**, managed by the Italian Agenzia delle Entrate, so client applications can retrieve real-estate quotation data without integrating directly with the public OMI web portal.

> Data source attribution: `Agenzia Entrate - OMI`.

## What It Does

OMI REST API Gateway is designed to act as a small backend gateway between applications and the Italian OMI services.

Typical use cases include:

- searching OMI quotation data by location;
- retrieving real-estate market value ranges for a municipality or OMI zone;
- exposing OMI data to web apps, internal tools, dashboards, or automation scripts;
- normalizing OMI portal responses into predictable JSON payloads.

## Background

OMI quotations provide minimum and maximum real-estate market and rental values by territorial zone, property type, and reference semester.

These quotations are useful as a broad market reference, but they are not a replacement for a detailed property appraisal. A professional valuation is still required when a precise estimate is needed.

## API

The exact endpoints may evolve with the implementation. A typical API shape is expected to look like this:

```http
GET /api/omi/quotations
```

Example query:

```http
GET /api/omi/quotations?province=MI&municipality=Milano&semester=2025-2&propertyType=abitazioni
```

Example response:

```json
{
  "source": "Agenzia Entrate - OMI",
  "province": "MI",
  "municipality": "Milano",
  "semester": "2025-2",
  "results": [
    {
      "zone": "B1",
      "description": "Central area",
      "propertyType": "abitazioni",
      "marketValue": {
        "min": 3500,
        "max": 5200,
        "unit": "EUR/m2"
      },
      "rentalValue": {
        "min": 12,
        "max": 20,
        "unit": "EUR/m2/month"
      }
    }
  ]
}
```

## Suggested Endpoints

```http
GET /health
GET /api/omi/regions
GET /api/omi/provinces
GET /api/omi/municipalities
GET /api/omi/zones
GET /api/omi/quotations
```

## Query Parameters

Common filters:

- `region`: Italian region name or code;
- `province`: province code, for example `MI`, `RM`, `NA`;
- `municipality`: municipality name;
- `zone`: OMI zone code;
- `semester`: reference semester, for example `2025-2`;
- `propertyType`: property category, for example `abitazioni`, `uffici`, `negozi`, `box`;
- `contractType`: `sale` or `rent`.

## Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd omi-rest-api-gateway
```

Install dependencies and start the service using the commands provided by the implementation stack.

For example:

```bash
# install dependencies
<package-manager> install

# run locally
<package-manager> run dev
```

The service should expose the API on a local HTTP port, for example:

```text
http://localhost:8080
```

## Configuration

Recommended environment variables:

```env
PORT=8080
OMI_BASE_URL=<omi-portal-base-url>
REQUEST_TIMEOUT_MS=30000
CACHE_TTL_SECONDS=86400
```

## Caching

OMI quotation data is published by semester and does not usually change frequently after publication. A cache layer is recommended to:

- reduce calls to the source portal;
- improve response time;
- protect the service from temporary upstream failures.

## Error Handling

The API should return predictable HTTP status codes:

- `200 OK`: request completed successfully;
- `400 Bad Request`: invalid or missing query parameters;
- `404 Not Found`: no matching OMI data found;
- `502 Bad Gateway`: upstream OMI portal error;
- `504 Gateway Timeout`: upstream request timed out.

Example error:

```json
{
  "error": "OMI_UPSTREAM_TIMEOUT",
  "message": "The OMI portal did not respond before the configured timeout."
}
```

## Development

Recommended project tasks:

```bash
# run tests
<package-manager> test

# run linting
<package-manager> run lint

# build
<package-manager> run build
```

## Legal And Data Notice

This project is not affiliated with Agenzia delle Entrate.

When using OMI data, cite the source as:

```text
Agenzia Entrate - OMI
```

OMI quotations represent broad market ranges and should not be treated as a formal appraisal or as a substitute for professional real-estate valuation.

## License

Add the project license here.
