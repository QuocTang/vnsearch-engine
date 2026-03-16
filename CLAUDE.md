# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vietnamese Semantic Search Engine (VnSearch) — a microservices-based system for semantic search over Vietnamese news articles. Uses TF-IDF vectorization with Qdrant vector database for similarity search.

## Architecture

Five services orchestrated via Docker Compose (`setup/docker-compose.yml`):

| Service | Tech | Port |
|---------|------|------|
| **irs_web** | Next.js 16, React 19, TailwindCSS 4 | 3000 |
| **irs_api** | FastAPI, Python 3.12, Scikit-learn | 8000 |
| **qdrant** | Qdrant vector DB | 6333/6334 |
| **n8n** | Workflow automation | 5678 |
| **postgres** | PostgreSQL 18 (n8n backend) | 5432 |

**Search flow:** Query → Vietnamese NLP preprocessing (Underthesea tokenization, stopword removal) → TF-IDF vectorization → Qdrant cosine similarity search → ranked results.

**Ingestion flow:** Excel files → Pandas processing → text preprocessing → TF-IDF model fitting → vectors uploaded to Qdrant.

## Common Commands

### Start all services
```bash
./setup/start.sh
# or: cd setup && docker-compose -p vnsearch-engine up -d
```

### Backend (irs_api)
```bash
cd microservices/irs_api
uv sync                    # Install dependencies
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Dev server
uv run pytest              # Run all tests
uv run pytest tests/test_api/  # Run specific test directory
uv run black .             # Format code
uv run ruff check .        # Lint
```

### Frontend (irs_web)
```bash
cd microservices/irs_web
pnpm install               # Install dependencies
pnpm dev                   # Dev server (port 3000)
pnpm build                 # Production build
pnpm lint                  # ESLint
```

### Build & Deploy Docker Images
```bash
./deploy/build_all.sh      # Build and push all images to Docker Hub
```

## Backend Structure (microservices/irs_api)

- `app/api/v1/` — API routes: `search.py` (POST /api/v1/search), `ingest.py` (POST /api/v1/ingest), `health.py`
- `app/services/` — Business logic: `nlp_processor.py` (Vietnamese NLP), `tfidf_service.py` (vectorization), `qdrant_service.py` (vector DB ops), `ingestion_service.py`
- `app/models/` — Pydantic request/response schemas
- `app/core/config.py` — Settings via pydantic-settings (env vars)
- `app/utils/` — Excel loader, stopwords loader
- `tests/` — pytest tests mirroring app structure

## Frontend Structure (microservices/irs_web)

- Next.js App Router (`app/`) with TypeScript strict mode
- `features/` — Feature modules (search UI)
- `components/` — Shared UI (Shadcn/Radix)
- `core/` — HTTP client, env utilities
- `store/` — Zustand state management
- `hooks/` — Custom React hooks
- Path alias: `@/*` maps to project root

## Key Configuration

- Backend env: `microservices/irs_api/.env` (Qdrant host/port, API host/port, data paths)
- Frontend env: `microservices/irs_web/.env.local` (API base URL)
- Docker Compose: `setup/docker-compose.yml` (uses external `main-network`)
- Commit messages are in Vietnamese with conventional prefixes (feat:, docs:, build:, fix:)
