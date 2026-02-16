# Kế hoạch triển khai IRS API

**Dự án**: Information Retrieval System API  
**Mục tiêu**: Xây dựng hệ thống tìm kiếm semantic cho bài báo tiếng Việt  
**Tech Stack**: Python 3.12, FastAPI, Qdrant, TF-IDF, Underthesea  
**Timeline**: 4-6 tuần  
**Last Updated**: 2026-02-16 08:51  
**Progress**: Phase 1 ✅ | Phase 2 ⏳ | Phase 3 ⬜ | Phase 4 ⬜ | Phase 5 ⬜

---

## 📋 Phase 1: Setup Môi Trường ✅ **COMPLETED** (2026-02-16)

### Tasks

- [x] **1.1. Cập nhật Dependencies**
  - Thêm FastAPI, Qdrant client, Pandas, Underthesea vào `pyproject.toml`
  - Run `uv sync` để install
  - Verify các packages import thành công
  - **Result**: ✅ 58 packages installed successfully

- [x] **1.2. Tạo Environment Configuration**
  - Tạo file `.env.example` với các biến cần thiết
  - Tạo `.env` từ template (git ignore)
  - Setup Qdrant connection parameters
  - **Result**: ✅ All environment variables documented

- [x] **1.3. Tạo cấu trúc thư mục**
  - Tạo các thư mục: `app/`, `app/api/`, `app/core/`, `app/services/`, `app/utils/`, `app/models/`
  - Tạo `models/` cho ML models
  - Tạo `tests/` cho unit tests
  - Tạo `docker/` cho Dockerfile
  - **Result**: ✅ 17 directories created with **init**.py files

- [x] **1.4. Setup Git Ignore**
  - Tạo `.gitignore` cho Python project
  - Ignore `.venv/`, `.env`, `models/*.pkl`, `__pycache__/`
  - **Result**: ✅ Git configuration complete

**Deliverables**: ✅ **ALL COMPLETED**

- ✅ Project structure hoàn chỉnh (17 directories)
- ✅ Dependencies installed (58 packages)
- ✅ Environment config ready (.env.example created)
- ✅ Git ignore configured
- ✅ All core packages verified (FastAPI, Qdrant, Pandas, Underthesea)

---

## 🔧 Phase 2: Core Services Development (Tuần 2-3)

### Tasks

- [ ] **2.1. Configuration Management**
  - File: `app/core/config.py`
  - Implement Pydantic Settings
  - Load environment variables
  - Validate config

- [ ] **2.2. Stopwords Loader**
  - File: `app/utils/stopwords_loader.py`
  - Load `vietnamese-stopwords.txt`
  - Cache trong memory
  - Unit test

- [ ] **2.3. Excel Data Loader**
  - File: `app/utils/excel_loader.py`
  - Load 3 Excel files (articles, categories, comments)
  - Merge data logic (join categories, count comments)
  - Create `full_text` field
  - Unit test với sample data

- [ ] **2.4. NLP Processor**
  - File: `app/services/nlp_processor.py`
  - Tokenization (underthesea)
  - Lowercase
  - Remove stopwords
  - **CRITICAL**: Ensure consistency
  - Unit test

- [ ] **2.5. TF-IDF Service**
  - File: `app/services/tfidf_service.py`
  - Train TF-IDF model
  - Save model (`joblib`)
  - Load model
  - Transform text to vector
  - Unit test

- [ ] **2.6. Qdrant Service**
  - File: `app/services/qdrant_service.py`
  - Connect to Qdrant
  - Create collection
  - Upsert vectors
  - Search with filters
  - Health check
  - Unit test (require Qdrant running)

**Deliverables**:

- ✅ 6 core services implemented và tested
- ✅ Unit test coverage > 80%

---

## 📊 Phase 3: Data Ingestion Pipeline (Tuần 3-4)

### Tasks

- [ ] **3.1. Ingestion Service**
  - File: `app/services/ingestion_service.py`
  - Orchestrate full ingestion flow:
    1. Load Excel data
    2. Merge và clean
    3. NLP preprocessing
    4. Train TF-IDF
    5. Transform to vectors
    6. Index to Qdrant
  - Logging và progress tracking

- [ ] **3.2. Standalone Ingestion Script**
  - File: `scripts/initial_ingest.py`
  - CLI tool để run ingestion
  - Useful cho debugging
  - Document usage

- [ ] **3.3. End-to-End Test**
  - Test với real data từ Excel files
  - Verify TF-IDF model saved
  - Verify Qdrant collection created
  - Verify all vectors indexed
  - Check data quality

**Deliverables**:

- ✅ Working ingestion pipeline
- ✅ TF-IDF model trained và saved
- ✅ Qdrant indexed với real data

---

## 🚀 Phase 4: API Development (Tuần 4-5)

### Tasks

- [ ] **4.1. Pydantic Models**
  - File: `app/models/request.py` - SearchRequest, IngestRequest
  - File: `app/models/response.py` - SearchResponse, ArticleResult

- [ ] **4.2. Health Check Endpoint**
  - File: `app/api/v1/health.py`
  - `GET /` endpoint
  - Check Qdrant connection
  - Return status JSON

- [ ] **4.3. Ingest Endpoint**
  - File: `app/api/v1/ingest.py`
  - `POST /api/v1/ingest`
  - Trigger ingestion pipeline
  - Return stats (docs count, dimension)
  - Admin only (optional auth)

- [ ] **4.4. Search Endpoint** ⭐ (Most Important)
  - File: `app/api/v1/search.py`
  - `POST /api/v1/search`
  - Process query:
    1. NLP preprocessing
    2. Transform to vector
    3. Search Qdrant
    4. Format results
  - Support category filter
  - Measure execution time

- [ ] **4.5. FastAPI App Initialization**
  - File: `main.py`
  - Create FastAPI app
  - Include routers
  - Setup CORS
  - Lifespan events (load model)
  - Run server

- [ ] **4.6. API Integration Tests**
  - Test all 3 endpoints
  - Test error handling
  - Test edge cases

**Deliverables**:

- ✅ 3 API endpoints working
- ✅ Swagger docs available
- ✅ Integration tests pass

---

## 🐳 Phase 5: Docker & Deployment (Tuần 5-6)

### Tasks

- [ ] **5.1. Dockerfile**
  - File: `docker/Dockerfile`
  - Multi-stage build
  - Python 3.12 Alpine base
  - Copy code và assets
  - Non-root user
  - Expose port 8000

- [ ] **5.2. Docker Compose Integration**
  - Update `setup/docker-compose.yml`
  - Add `irs_api` service
  - Depends on `qdrant`
  - Network config
  - Volume for models

- [ ] **5.3. Docker Testing**
  - Build image
  - Run container
  - Test API endpoints
  - Test Qdrant connection

- [ ] **5.4. Documentation**
  - Update README với deployment instructions
  - API documentation
  - Environment variables guide
  - Troubleshooting guide

**Deliverables**:

- ✅ Dockerized application
- ✅ Docker Compose working
- ✅ Production-ready deployment
- ✅ Complete documentation

---

## 📈 Performance Targets

| Metric           | Target        | Verification        |
| ---------------- | ------------- | ------------------- |
| Search latency   | < 500ms       | Load testing với ab |
| TF-IDF transform | < 100ms       | Unit test timing    |
| Qdrant search    | < 50ms        | Service test timing |
| API throughput   | > 100 req/s   | Apache Bench        |
| Relevance        | Manual verify | Sample queries      |

---

## 🧪 Testing Strategy

### Unit Tests

- All services in `app/services/`
- All utilities in `app/utils/`
- Coverage target: > 80%

### Integration Tests

- API endpoints
- End-to-end ingestion
- End-to-end search

### Manual Tests

- Search quality verification
- Category filtering
- Edge cases handling

### Load Tests

- Apache Bench for throughput
- Response time under load

---

## 📝 Documentation Checklist

- [ ] API documentation (Swagger/ReDoc)
- [ ] README với setup instructions
- [ ] Environment variables guide
- [ ] Deployment guide (Docker)
- [ ] Testing guide
- [ ] Troubleshooting FAQ
- [ ] Architecture diagram

---

## ⚠️ Risks & Mitigations

| Risk                       | Impact              | Mitigation                      |
| -------------------------- | ------------------- | ------------------------------- |
| TF-IDF model quá lớn       | High memory usage   | Monitor size, tuning parameters |
| Qdrant connection unstable | API failures        | Retry logic, health checks      |
| NLP inconsistency          | Poor search quality | Shared preprocessing function   |
| Slow search performance    | User experience     | Profiling, optimization         |
| Excel data quality         | Indexing errors     | Data validation, error handling |

---

## 🎯 Success Criteria

- ✅ All 3 API endpoints working correctly
- ✅ Search returns relevant results for Vietnamese queries
- ✅ Category filtering works
- ✅ Performance targets met (< 500ms response)
- ✅ Docker deployment successful
- ✅ All tests passing
- ✅ Documentation complete

---

**Ngày tạo**: 2026-02-16  
**Phiên bản**: 1.0
