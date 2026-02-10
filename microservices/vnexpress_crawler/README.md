# VnExpress Crawler API

A FastAPI-based crawler for VnExpress news categories and articles.

## Setup

```bash
# Install dependencies
uv sync

# Run the API
uv run main.py
```

## Running

The API will start at `http://localhost:8000`

### Documentation

- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: `swagger.json` (auto-generated on startup)

## Endpoints

### Health Check
- `GET /health` - Check API status

### Categories
- `GET /api/v1/categories/` - Get all categories
- `GET /api/v1/categories/{category_id}` - Get specific category
- `GET /api/v1/categories/search?q=query` - Search categories

### Articles (Not yet implemented)
- `GET /api/v1/articles/category/{category_id}` - Get articles by category
- `GET /api/v1/articles/{article_id}` - Get article details
- `GET /api/v1/articles/{article_id}/comments` - Get article comments

## Configuration

Copy `.env.example` to `.env` and update values if needed:

```bash
cp .env.example .env
```

### Environment Variables

- `DEBUG` - Enable debug mode
- `API_TITLE` - API title
- `API_VERSION` - API version
- `VNEXPRESS_MICROSERVICE_URL` - VnExpress microservice URL
- `REQUEST_TIMEOUT` - HTTP request timeout (seconds)
- `CACHE_CATEGORIES` - Category cache TTL (seconds)
- `CACHE_ARTICLES` - Article cache TTL (seconds)

## Features

- ✅ Fetch all VnExpress categories
- ✅ Search categories by name
- ✅ In-memory caching with TTL
- ✅ Auto-generated Swagger documentation
- ✅ Structured logging
- ❌ Article fetching (VnExpress blocks direct API access)

## Generated Files

- `swagger.json` - OpenAPI 3.0 schema (auto-generated on startup)
