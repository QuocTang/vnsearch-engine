# IRS API - Tài liệu tích hợp

**Base URL**: `http://localhost:8000`  
**Version**: 1.0.0  
**Format**: JSON

---

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /`

**Description**: Kiểm tra trạng thái service

**Request**: Không có body

**Response** (200 OK):

```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "model_loaded": true
}
```

**Response Fields**:

- `status` (string): `"healthy"` hoặc `"unhealthy"`
- `qdrant_connected` (boolean): Kết nối Qdrant database
- `model_loaded` (boolean): TF-IDF model đã load

---

### 2. Search Articles

**Endpoint**: `POST /api/v1/search`

**Description**: Tìm kiếm semantic articles theo query tiếng Việt

**Request Headers**:

```
Content-Type: application/json
```

**Request Body**:

```json
{
  "query": "công nghệ AI",
  "limit": 10,
  "category_filter": "Khoa học"
}
```

**Request Parameters**:
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `query` | string | **Yes** | 1-500 chars | Từ khóa tìm kiếm tiếng Việt |
| `limit` | integer | No | 1-100 | Số kết quả trả về (default: 10) |
| `category_filter` | string | No | - | Lọc theo category |

**Available Categories**: `"Khoa học"`, `"Ý kiến"`, `"Giáo dục"`, `"Sức khỏe"`, `"Thời sự"`, `"Giải trí"`, `"Đời sống"`

**Response** (200 OK):

```json
{
  "query": "công nghệ AI",
  "processed_query": "công_nghệ",
  "total_results": 2,
  "execution_time_ms": 54.32,
  "results": [
    {
      "id": 1635,
      "score": 0.465,
      "article_id": 4828056,
      "title": "Những chính sách khoa học công nghệ được kỳ vọng năm 2025",
      "summary": "Năm 2025, Chính phủ, Bộ Khoa học và Công nghệ xác định...",
      "url": "https://vnexpress.net/...",
      "category_name": "Khoa học",
      "comment_count": 1
    }
  ]
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Query gốc từ request |
| `processed_query` | string | Query sau khi xử lý NLP (tokenized) |
| `total_results` | integer | Số lượng kết quả tìm được |
| `execution_time_ms` | float | Thời gian xử lý (milliseconds) |
| `results` | array | Danh sách articles |

**Article Object**:
| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Vector ID trong database |
| `score` | float | Độ tương đồng semantic (0.0-1.0, cao hơn = relevant hơn) |
| `article_id` | integer | ID bài viết gốc |
| `title` | string | Tiêu đề bài viết |
| `summary` | string | Tóm tắt nội dung |
| `url` | string | URL bài viết đầy đủ |
| `category_name` | string | Tên danh mục |
| `comment_count` | integer | Số lượng comments |

**Error Response** (400 Bad Request):

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "query"],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

**Error Response** (500 Internal Server Error):

```json
{
  "detail": "Internal Server Error"
}
```

---

### 3. Trigger Ingestion (Admin Only)

**Endpoint**: `POST /api/v1/ingest`

**Description**: Trigger data ingestion pipeline (re-index toàn bộ data)

**Request**: Không có body

**Response** (200 OK):

```json
{
  "status": "success",
  "message": "Data ingestion completed successfully",
  "articles_count": 2232,
  "vector_dimension": 3740,
  "collection_name": "articles",
  "collection_info": {
    "points_count": 2232,
    "status": "green"
  }
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"success"` hoặc `"error"` |
| `message` | string | Mô tả kết quả |
| `articles_count` | integer | Số lượng articles đã index |
| `vector_dimension` | integer | Số chiều của vector (features) |
| `collection_name` | string | Tên collection trong Qdrant |
| `collection_info` | object | Metadata của collection |

**⚠️ Warning**: Endpoint này chạy 30-60 giây. Không nên expose cho end users.

---

## HTTP Status Codes

| Code | Meaning               | Khi nào                                          |
| ---- | --------------------- | ------------------------------------------------ |
| 200  | OK                    | Request thành công                               |
| 400  | Bad Request           | Validation error (query rỗng, limit > 100, etc.) |
| 500  | Internal Server Error | Lỗi server (model không load, Qdrant down, etc.) |

---

## CORS

API enable CORS cho tất cả origins (development):

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: *`
- `Access-Control-Allow-Headers: *`

**Production**: Sẽ restrict origins khi deploy.

---

## Performance Metrics

| Endpoint              | Response Time         |
| --------------------- | --------------------- |
| `GET /`               | < 10ms                |
| `POST /api/v1/search` | 50-300ms (avg: 200ms) |
| `POST /api/v1/ingest` | 30-60 seconds         |

**Lưu ý**: Search execution time có trong response field `execution_time_ms`

---

## Interactive Documentation

**Swagger UI**: http://localhost:8000/docs  
**ReDoc**: http://localhost:8000/redoc

→ Test API trực tiếp từ browser và xem schema chi tiết

---

## Production Deployment

Khi deploy production, cần update:

1. **Base URL**: Thay `localhost:8000` bằng domain thực
2. **CORS**: Config allowed origins
3. **Authentication**: Thêm API key hoặc JWT (nếu cần)

---

**Last Updated**: 2026-02-16  
**API Version**: 1.0.0
