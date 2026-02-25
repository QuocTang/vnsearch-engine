# Cấu trúc Dự án Backend (IRS API)

Dưới đây là cấu trúc thư mục và tệp tin của service `irs_api`, được tổ chức theo kiến trúc Clean Architecture/Modular để dễ dàng mở rộng và bảo trì.

```
irs_api/
├── app/                        # Source code chính của ứng dụng
│   ├── __init__.py
│   ├── api/                    # Chứa các Controller/Route Handlers
│   │   ├── __init__.py
│   │   └── v1/                 # API Version 1
│   │       ├── __init__.py
│   │       ├── dependencies.py # Các dependency injection
│   │       ├── health.py       # API Health check
│   │       ├── ingest.py       # API Trigger Ingestion
│   │       └── search.py       # API Search
│   ├── core/                   # Cấu hình cốt lõi của ứng dụng
│   │   ├── __init__.py
│   │   └── config.py           # Quản lý biến môi trường, cấu hình chung
│   ├── models/                 # Chứa các Pydantic Models (Schemas)
│   │   ├── __init__.py
│   │   ├── request.py          # Request Body schemas
│   │   └── response.py         # Response Body schemas
│   ├── services/               # Chứa Business Logic
│   │   ├── __init__.py
│   │   ├── ingestion_service.py # Logic nạp dữ liệu (ETL)
│   │   ├── nlp_processor.py    # Logic xử lý NLP (Tiền xử lý)
│   │   ├── qdrant_service.py   # Logic tương tác với Qdrant
│   │   └── tfidf_service.py    # Logic Vectorization (TF-IDF)
│   └── utils/                  # Các hàm tiện ích
│       ├── __init__.py
│       ├── excel_loader.py     # Đọc file Excel
│       └── stopwords_loader.py # Đọc file Stopwords
├── assets/                     # Tài nguyên tĩnh (Dữ liệu đầu vào)
│   ├── excel/                  # Chứa file Excel dữ liệu nguồn
│   │   ├── articles.xlsx
│   │   ├── categories.xlsx
│   │   └── comments.xlsx
│   └── txt/                    # Chứa file text phụ trợ
│       └── vietnamese-stopwords.txt
├── models/                     # Thư mục chứa Model đã huấn luyện (Artifacts)
│   ├── .gitkeep               # Giữ thư mục trong git
│   └── tfidf_vectorizer.pkl    # Model TF-IDF được serialize
├── scripts/                    # Các script chạy rời (không qua API)
│   └── initial_ingest.py       # Script chạy ingestion lần đầu
├── tests/                      # Unit Tests
│   └── __init__.py
├── .dockerignore
├── .env                        # Environment variables (local)
├── .env.example                # Environment variables template
├── .gitignore
├── Dockerfile                  # File build Docker image
├── main.py                     # Entry point của ứng dụng (chạy Uvicorn)
├── pyproject.toml              # Quản lý dependencies (Poetry/UV)
├── README.md                   # Tài liệu hướng dẫn sử dụng
└── uv.lock                     # File lock version của dependencies
```

## Mô tả chi tiết các thành phần

### 1. `app/` (Application Core)
Đây là nơi chứa toàn bộ logic của ứng dụng.

- **`api/`**: Nơi định nghĩa các endpoint. `v1/` giúp quản lý phiên bản API.
  - `health.py`: Kiểm tra trạng thái service và kết nối Qdrant.
  - `ingest.py`: Endpoint để admin kích hoạt quá trình nạp dữ liệu.
  - `search.py`: Endpoint chính phục vụ tìm kiếm.
- **`core/`**: Chứa `config.py` để load các biến môi trường (như Qdrant URL, Database path) bằng `pydantic-settings`, giúp code không bị hardcode.
- **`models/`**: Định nghĩa dữ liệu đầu vào/đầu ra (DTO) bằng Pydantic. Giúp validate dữ liệu tự động.
- **`services/`**: Tách biệt logic nghiệp vụ khỏi Controller (API).
  - `nlp_processor.py`: Chứa hàm `preprocess_text` (clean, tokenize, remove stopwords).
  - `tfidf_service.py`: Quản lý việc load/save model TF-IDF và transform văn bản thành vector.
  - `qdrant_service.py`: Wrapper class để gọi các hàm của `qdrant-client` (search, upload).
  - `ingestion_service.py`: Orchestrator, gọi các service khác để thực hiện luồng ETL đầy đủ.
- **`utils/`**: Các hàm hỗ trợ đọc file, xử lý chuỗi đơn giản.

### 2. `assets/` (Static Resources)
Nơi chứa dữ liệu thô. Trong môi trường production, folder này có thể được mount từ bên ngoài vào container.

### 3. `models/` (Artifacts)
Nơi lưu trữ file model `.pkl` sau khi huấn luyện. Folder này cần được persist (lưu trữ lâu dài) hoặc tạo lại mỗi khi chạy Ingestion.

### 4. `scripts/`
Chứa các script tiện ích, ví dụ `initial_ingest.py` có thể được gọi khi container khởi động để nạp dữ liệu tự động mà không cần gọi API.

### 5. `tests/`
Cấu trúc test tương ứng với cấu trúc code trong `app/` để dễ dàng viết Unit Test.

---
**Lưu ý:** Cấu trúc này đảm bảo tính "Separation of Concerns" (Tách biệt mối quan tâm), giúp code dễ đọc, dễ test và dễ mở rộng sau này.
