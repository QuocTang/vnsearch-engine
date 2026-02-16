# TÀI LIỆU YÊU CẦU KỸ THUẬT BACKEND (BE-PRD)

**Dự án:** Hệ Truy hồi Thông tin Tiếng Việt (IRS) sử dụng Vector Space Model
**Công nghệ:** Python FastAPI, Qdrant, Docker, Scikit-learn (TF-IDF), Underthesea.

---

## 1. Bức tranh tổng quan (System Architecture)

Hệ thống hoạt động theo mô hình **Client-Server** được đóng gói trong **Docker Compose**.

### Sơ đồ kiến trúc logic:

1. **Client (Frontend):** Gửi HTTP Request (Query tìm kiếm) đến Backend.
2. **Backend (Python API):**

- Đóng vai trò trung tâm xử lý.
- Chứa **NLP Pipeline** (Tách từ, Stopwords).
- Chứa **Vector Model** (TF-IDF Vectorizer đã được huấn luyện).

3. **Database (Qdrant):**

- Lưu trữ hàng nghìn Vector (đại diện cho bài báo).
- Lưu trữ Payload (Thông tin bài báo, danh mục, số bình luận).
- Thực hiện thuật toán tìm kiếm tương đồng (Cosine Similarity).

4. **Data Source (Excel):** Nguồn dữ liệu tĩnh được nạp vào hệ thống khi khởi động hoặc qua API kích hoạt.

---

## 2. Luồng xử lý dữ liệu (Data Flows)

Đây là 2 luồng quan trọng nhất backend cần xử lý.

### 2.1. Luồng nạp dữ liệu (Data Ingestion Pipeline)

_Mục đích: Đọc Excel, làm sạch, vector hóa và lưu vào Qdrant._

1. **Load Data:**

- Đọc `Articles.xlsx`.
- Đọc `Categories.xlsx` -> Tạo dictionary `{category_id: category_name}`.
- Đọc `Comments.xlsx` -> Group by `article_id` -> Count số lượng comment.

2. **Merge & Clean:**

- Join `category_name` vào Article.
- Join `comment_count` vào Article.
- Tạo field `full_text` = `title` + " " + `summary`.

3. **NLP Preprocessing:**

- Input: `full_text`.
- Action: Tokenize (tách từ tiếng Việt) -> Lowercase -> Remove Stopwords (từ file `vietnamese-stopwords.txt`).

4. **Vectorization (Training):**

- Fit model `TfidfVectorizer` trên toàn bộ tập dữ liệu đã tiền xử lý.
- **Quan trọng:** Lưu model này lại (dùng `pickle` hoặc `joblib`) để dùng cho lúc Search.
- Transform toàn bộ văn bản thành các Vector số thực.

5. **Indexing:**

- Upload Vector + Payload (Title, URL, Category, CommentCount) vào Qdrant Collection.

### 2.2. Luồng tìm kiếm (Search Flow)

_Mục đích: Nhận từ khóa và trả về kết quả._

1. **Receive Request:** API nhận `query` string (ví dụ: "giá xăng dầu hôm nay").
2. **Query Preprocessing:**

- Áp dụng quy trình NLP y hệt bước Ingestion (Tokenize -> Stopwords).

3. **Vectorization (Inference):**

- Load model TF-IDF đã lưu.
- Transform `query` đã xử lý thành 1 Vector (không được fit lại model).

4. **Semantic Search:**

- Gửi Vector này sang Qdrant.
- Qdrant tìm Top K vector gần nhất (dựa trên Cosine Similarity).
- (Optional) Áp dụng Filter nếu người dùng chọn Danh mục.

5. **Response:** Trả về danh sách bài báo (JSON) kèm điểm số tương đồng (Score).

---

## 3. Thiết kế API (API Specifications)

Hệ thống cần tối thiểu **03 API** chính để hoạt động hoàn chỉnh.

### API 1: Kiểm tra hệ thống (Health Check)

- **Method:** `GET`
- **Endpoint:** `/`
- **Mục đích:** Đảm bảo Backend và Qdrant đã kết nối thành công.
- **Response:**

```json
{ "status": "ok", "qdrant_connection": true }
```

### API 2: Kích hoạt nạp dữ liệu (Trigger Ingestion)

- **Method:** `POST`
- **Endpoint:** `/api/v1/ingest`
- **Mục đích:** Admin gọi API này để hệ thống đọc file Excel và nạp lại dữ liệu vào Qdrant (Thường chạy 1 lần đầu hoặc khi cập nhật Excel).
- **Response:**

```json
{
  "message": "Ingestion successful",
  "total_documents": 1500,
  "vector_dimension": 5000
}
```

### API 3: Tìm kiếm (Search) - **Quan Trọng Nhất**

- **Method:** `POST` (hoặc `GET`)
- **Endpoint:** `/api/v1/search`
- **Body Request:**

```json
{
  "query": "tình hình biến đổi khí hậu",
  "limit": 10,
  "category_filter": "Môi trường" // Optional
}
```

- **Mục đích:** Xử lý luồng tìm kiếm và trả về kết quả.
- **Response:**

```json
{
  "results": [
    {
      "article_id": 101,
      "title": "Biến đổi khí hậu ảnh hưởng đến ĐBSCL",
      "summary": "Nước biển dâng cao khiến...",
      "category": "Môi trường",
      "comment_count": 15,
      "score": 0.89, // Độ tương đồng
      "url": "https://..."
    }
    // ... các kết quả khác
  ],
  "execution_time": 0.05
}
```

---

## 4. Chi tiết cấu trúc dữ liệu (Data Structure)

Để Backend giao tiếp hiệu quả, cần quy định rõ cấu trúc dữ liệu tại các điểm nút.

### 4.1. Cấu trúc Payload trong Qdrant (Point)

Mỗi "điểm" dữ liệu trong Qdrant sẽ lưu:

- **ID:** `article_id` (Integer)
- **Vector:** `[0.01, 0.05, ...]` (Sparse hoặc Dense Vector từ TF-IDF)
- **Payload (Metadata):**

```json
{
  "title": "String",
  "summary": "String",
  "url": "String",
  "thumbnail_url": "String",
  "published_at": "String (ISO Date)",
  "category_name": "String", // Dùng để filter
  "comment_count": "Integer" // Dùng để hiển thị độ hot
}
```

### 4.2. Cấu trúc Stopwords

Sử dụng file text `vietnamese-stopwords.txt`, mỗi dòng là một từ dừng.

- Ví dụ: `và`, `của`, `là`, `những`, `cái`, `thì`...

---

## 5. Yêu cầu phi chức năng (Non-functional Requirements)

1. **Hiệu năng:**

- Thời gian vector hóa query: < 100ms.
- Thời gian tìm kiếm Qdrant: < 50ms.
- Tổng thời gian phản hồi API: < 500ms.

2. **Độ chính xác:**

- Kết quả trả về phải có nội dung liên quan đến từ khóa (không cần khớp chính xác từng từ mà khớp theo ngữ cảnh vector).

3. **Khả năng mở rộng:**

- Cấu hình Docker phải mount volume để dữ liệu Qdrant không bị mất khi restart container.

---

## 6. Stack công nghệ chi tiết (Cho code Python)

- **Framework:** `FastAPI`.
- **Data Processing:** `Pandas` (xử lý Excel), `Numpy`.
- **NLP:** `Underthesea` (word_tokenize).
- **ML Model:** `Scikit-learn` (`TfidfVectorizer`).
- **DB Client:** `qdrant-client`.
- **Environment:** `Python`, `Docker`.
