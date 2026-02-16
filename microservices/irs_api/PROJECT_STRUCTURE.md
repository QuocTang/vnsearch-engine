# CẤU TRÚC DỰ ÁN IRS API

## 📂 Cấu trúc thư mục dự kiến

```
irs_api/
│
├── .python-version                    # Python 3.12
├── .venv/                             # Virtual environment
├── .env                               # Environment variables
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore
│
├── pyproject.toml                     # Project config & dependencies
├── uv.lock                            # Lock file
├── README.md                          # Tài liệu yêu cầu kỹ thuật
│
├── main.py                            # Entry point chạy ứng dụng
│
├── app/                               # Main application
│   ├── __init__.py
│   │
│   ├── api/                           # API endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── health.py              # GET / - Health check
│   │       ├── ingest.py              # POST /api/v1/ingest
│   │       └── search.py              # POST /api/v1/search
│   │
│   ├── core/                          # Core config
│   │   ├── __init__.py
│   │   ├── config.py                  # Settings, ENV vars
│   │   └── dependencies.py            # FastAPI dependencies
│   │
│   ├── models/                        # Pydantic models
│   │   ├── __init__.py
│   │   ├── request.py                 # Request schemas
│   │   └── response.py                # Response schemas
│   │
│   ├── services/                      # Business logic
│   │   ├── __init__.py
│   │   ├── nlp_processor.py           # NLP preprocessing
│   │   ├── tfidf_service.py           # TF-IDF vectorization
│   │   ├── qdrant_service.py          # Qdrant client operations
│   │   └── ingestion_service.py       # Data ingestion pipeline
│   │
│   └── utils/                         # Utilities
│       ├── __init__.py
│       ├── excel_loader.py            # Load Excel files
│       └── stopwords_loader.py        # Load stopwords
│
├── assets/                            # Data resources (hiện tại)
│   ├── excel/
│   │   ├── articles.xlsx
│   │   ├── categories.xlsx
│   │   └── comments.xlsx
│   └── txt/
│       └── vietnamese-stopwords.txt
│
├── models/                            # Saved ML models
│   └── tfidf_vectorizer.pkl           # Trained TF-IDF model
│
├── tests/                             # Unit tests
│   ├── __init__.py
│   ├── test_api/
│   │   ├── test_health.py
│   │   ├── test_ingest.py
│   │   └── test_search.py
│   ├── test_services/
│   │   ├── test_nlp_processor.py
│   │   └── test_tfidf_service.py
│   └── conftest.py                    # Pytest fixtures
│
├── scripts/                           # Utility scripts
│   └── initial_ingest.py              # Script nạp data lần đầu
│
└── docker/                            # Docker files
    ├── Dockerfile                     # Docker image
    └── .dockerignore

```

## 📝 Mô tả ngắn gọn

### `app/api/v1/` - API Endpoints

- **health.py**: Kiểm tra kết nối hệ thống
- **ingest.py**: Nạp dữ liệu từ Excel vào Qdrant
- **search.py**: API tìm kiếm chính

### `app/core/` - Core Configuration

- **config.py**: Settings (Qdrant URL, ports, etc.)
- **dependencies.py**: Shared dependencies cho FastAPI

### `app/models/` - Data Models

- **request.py**: SearchRequest, IngestRequest
- **response.py**: SearchResponse, IngestResponse

### `app/services/` - Business Logic

- **nlp_processor.py**: Tokenize, lowercase, remove stopwords
- **tfidf_service.py**: Train/load TF-IDF model, transform text
- **qdrant_service.py**: Connect, create collection, upsert, search
- **ingestion_service.py**: Load Excel → Process → Index to Qdrant

### `app/utils/` - Utilities

- **excel_loader.py**: Read Excel với pandas
- **stopwords_loader.py**: Load danh sách stopwords

### `models/` - ML Models

- **tfidf_vectorizer.pkl**: TF-IDF model đã train

### `tests/` - Testing

- Unit tests cho từng module

---

**Ngày tạo**: 2026-02-16  
**Phiên bản**: 0.1.0
