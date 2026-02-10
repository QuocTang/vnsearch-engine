# Kế hoạch thu thập dữ liệu VNExpress - Phiên bản chuẩn (v2)

**API Base URL**: `https://apache-hive.onrender.com`  
**Status**: ✅ Hoạt động 100% - Tested on 2025-12-11

---

## 1. Mục tiêu

- Thu thập **data thô** từ VNExpress qua API crawl service
- Tách 3 loại dữ liệu: **categories**, **articles**, **comments**
- Ghi ra **file Excel** (multiple sheets) và upload lên **Google Drive** (qua n8n)

---

## 2. Cấu trúc dữ liệu & Excel

### 2.1 Categories (Sheet: `categories`)

**Endpoint**: `GET /api/v1/categories/`

**Response Structure**:

```json
{
  "total": 2366,
  "data": {
    "1001005": {
      "id": "1001005",
      "url": "/thoi-su",
      "name": "Thời sự",
      "parent_id": null
    }
  }
}
```

**Excel Columns**:
| Cột | Nguồn | Loại | Ghi chú |
|-----|-------|------|---------|
| `category_id` | `id` | TEXT | Primary Key |
| `category_url` | `url` | TEXT | ví dụ: `/thoi-su` |
| `category_name` | `name` | TEXT | Tên danh mục |
| `parent_id` | `parent_id` | TEXT/NULL | NULL = root category |
| `level` | Computed | TEXT | `root` nếu parent_id=null, else `child` |
| `crawled_at` | Hệ thống | DATETIME | Thời điểm crawl (ISO 8601) |
| `status` | Hệ thống | TEXT | `active` |

**Crawl Strategy**:

- Chạy 1 lần/ngày (định kỳ, 02:00 UTC)
- Gọi endpoint duy nhất, lấy hết tất cả categories (~2366 items)
- Overwrite file cũ (snapshot daily)

---

### 2.2 Articles (Sheet: `articles`)

**Endpoints** (3 loại, có thể kết hợp):

1. `GET /api/v1/articles/category/{id}?limit=50&offset=0` (GW API - fast)
2. `GET /api/v1/articles/category-paginated/{url}?page=1&limit=50` (Scraping - pagination)
3. `GET /api/v1/articles/category-date/{id}?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD&page=1&limit=50` (Scraping - date filter)

**Response Structure** (from endpoint 1):

```json
{
  "status": "success",
  "total": 2,
  "limit": 2,
  "offset": 0,
  "data": [
    {
      "id": "4992485",
      "title": "Gợi ý quà tặng cao cấp cho doanh nhân",
      "url": "https://vnexpress.net/goi-y-qua-tang-cao-cap-cho-doanh-nhan-4992485.html",
      "summary": "Vertu Việt Nam cung cấp nhiều sản phẩm...",
      "thumbnail_url": "https://i-kinhdoanh.vnecdn.net/2025/12/11/...",
      "published_at": "2025-12-11T04:00:00",
      "category_id": "1000000"
    }
  ]
}
```

**Response Structure** (from endpoint 2 - paginated):

```json
{
  "status": "success",
  "total": 2,
  "limit": 2,
  "offset": 0,
  "data": [
    {
      "id": "4992470",
      "title": "Chủ tịch Hà Nội...",
      "url": "https://vnexpress.net/...",
      "summary": "...",
      "thumbnail_url": "https://...",
      "published_at": null,
      "category_id": "1001002"
    }
  ]
}
```

**Response Structure** (from endpoint 3 - date filter):

```json
{
  "status": "success",
  "total": 29,
  "limit": 100,
  "offset": 0,
  "data": [
    {
      "id": "4992329",
      "title": "Thẩm phán ngăn ông Trump điều vệ binh tới Los Angeles",
      "url": "https://vnexpress.net/tham-phan-ngan-ong-trump-dieu-ve-binh-toi-los-angeles-4992329.html",
      "summary": "Thẩm phán liên bang ngăn Tổng thống Trump điều Vệ binh Quốc gia tới Los Angeles và yêu cầu trao lại quyền kiểm soát lực lượng này cho Thống đốc California.",
      "thumbnail_url": "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
      "published_at": null,
      "category_id": "1001002"
    }
  ]
}
```

**Excel Columns**:
| Cột | Loại | Ghi chú |
|-----|------|---------|
| `article_id` | TEXT | Primary Key, từ `id` |
| `category_id` | TEXT | Nullable (null từ scraping endpoints) |
| `title` | TEXT | Tiêu đề bài viết |
| `summary` | TEXT | Mô tả ngắn |
| `url` | TEXT | Link đầy đủ |
| `thumbnail_url` | TEXT | Link ảnh (nullable) |
| `published_at` | DATETIME | Nullable (null từ scraping endpoints) |
| `source_endpoint` | TEXT | `gw_api` \| `category_paginated` \| `category_date` |
| `page_no` | INTEGER | Số trang (nếu dùng pagination) |
| `crawled_at` | DATETIME | Thời điểm crawl |

**Crawl Strategy** (Recommended for 2000+ categories):

**✅ Phương án 2: Daily Date Range + Category Loop (BEST)**

- **Endpoint**: `GET /api/v1/articles/category-date/{id}?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD&page=1&limit=50`
- **Flow**:
  1. Daily schedule (03:00 UTC): Lấy articles của **ngày hôm nay** hoặc **7 ngày gần đây**
  2. Loop tất cả ~2366 categories với `from_date` và `to_date`
  3. Mỗi category: Pagination `page=1, 2, 3...` cho đến hết (`total`)
  4. Batch categories: 50-100 categories/batch để tránh overload
  5. Delay: 100-200ms giữa requests

- **Ưu điểm**:
  - ✅ Dễ kiểm soát volume (chỉ lấy N ngày gần đây, không quá nhiều)
  - ✅ Incremental sync tự động (hôm nay chỉ có data hôm nay)
  - ✅ Có thể rerun multiple times, dedup by `article_id` ngoài
  - ✅ Dễ monitor (segment theo ngày)
  - ✅ Performance: ~2-3 giờ/ngày (2366 categories × ~0.5-1 article/day/category)

- **Nhược điểm**:
  - ❌ `published_at=null` (nhưng có `crawled_at` để track)
  - ❌ Chậm hơn GW API, nhưng manageable

- **Excel mapping**: Thêm cột `date_range` = `{from_date}_{to_date}` để track

---

**❌ Phương án 1: GW API (NOT RECOMMENDED for 2000+ categories)**

- Endpoint: `GET /api/v1/articles/category/{id}?limit=50&offset=0`
- Vấn đề: ~2-3 giờ/run, quá nhiều data, khó kiểm soát
- Nên dùng chỉ khi cần full sync lần đầu

---

**📊 Giải pháp hybrid** (Recommended):

**Phase 1 (tuần 1)**: Full sync ngày hôm nay
```
- Loop 2366 categories
- from_date = 2025-12-11, to_date = 2025-12-11
- Lấy tất cả articles của ngày 11/12
```

**Phase 2+ (hàng ngày)**: Incremental sync
```
- Mỗi ngày 03:00 UTC: Lấy articles của ngày đó
- from_date = TODAY, to_date = TODAY
- Auto-append vào Excel
- Dedup by article_id nếu cần
```

**Optional**: Weekly backfill 7 ngày gần đây
```
- Hàng tuần (Thứ 2 04:00 UTC):
- from_date = TODAY - 7 days, to_date = TODAY
- Catch missing articles nếu có
```

---

### 2.3 Comments (Sheet: `comments`)

**Endpoint**: `GET /api/v1/articles/{id}/comments?object_id={id}&limit=100&sort_by=like`

**Response Structure**:

```json
{
  "status": "success",
  "total": 5,
  "limit": 5,
  "offset": 0,
  "data": [
    {
      "id": "61769917",
      "author": "Vu Lam",
      "content": "Tôi phải chia sẽ ngay bài viết này cho vợ, kkk.",
      "created_at": "05:38 2/12",
      "likes": 246
    },
    {
      "id": "61770351",
      "author": "lethithuhangkh",
      "content": "Có vài ba cọc ba đồng, tiền nhà điện nước gas rồi nuôi 2 con ăn học còn chẳng đủ...",
      "created_at": "07:10 2/12",
      "likes": 216
    }
  ]
}
```

**Excel Columns**:
| Cột | Loại | Ghi chú |
|-----|------|---------|
| `article_id` | TEXT | Foreign Key tới articles (tham số input) |
| `comment_id` | TEXT | Primary Key từ `id` |
| `author` | TEXT | Tên tác giả bình luận |
| `content` | TEXT | Nội dung bình luận (dài, lưu CLOB) |
| `created_at` | TEXT | Ngày tạo (format: "HH:mm DD/MM") |
| `likes` | INTEGER | Số lượt thích |
| `sort_by` | TEXT | `like` \| `newest` \| `oldest` (ghi phương thức crawl) |
| `crawled_at` | DATETIME | Thời điểm crawl (ISO 8601) |

**Crawl Strategy**:

- Lấy danh sách top N `article_id` từ sheet `articles` (ưu tiên articles mới/hot)
- Loop từng article, gọi endpoint với `sort_by=like` (top comments)
- Pagination: `offset = 0, 100, 200...` cho đến hết (`total`)
- Performance: ~500ms/article (test article ID: 4988419 → 5 comments)
- Recommendation: **Giai đoạn 1 bỏ qua** (non-critical), thêm vào giai đoạn 2 nếu cần
- Note: `created_at` từ API là short format ("HH:mm DD/MM"), cần parse/store as-is hoặc convert

---

## 3. n8n Workflow Specs

### 3.1 Flow: Daily Categories Sync

**Trigger**: Cron (hàng ngày 02:00 UTC)

**Steps**:

1. **Trigger - Cron**: `0 2 * * *`
2. **HTTP Request**: `GET https://apache-hive.onrender.com/api/v1/categories/`
3. **Code** (Transform to rows):
   ```js
   // Flatten dict to array
   const data = items[0].json.data;
   const rows = Object.entries(data).map(([id, cat]) => ({
     category_id: id,
     category_url: cat.url,
     category_name: cat.name,
     parent_id: cat.parent_id || "",
     level: cat.parent_id ? "child" : "root",
     crawled_at: new Date().toISOString(),
     status: "active",
   }));
   return rows.map((row) => ({ json: row }));
   ```
4. **Spreadsheet**: Create/Overwrite `categories.xlsx` (mode: OVERWRITE)
5. **Google Drive**: Upload with name `vnexpress_categories_{{$now.toFormat("yyyy-MM-dd_HHmmss")}}.xlsx`

---

### 3.2 Flow: Daily Articles Sync (Date Range + Incremental)

**Trigger**: Cron (hàng ngày 03:00 UTC) - sau categories sync

**Steps**:

1. **Trigger - Cron**: `0 3 * * *`
2. **Get Categories**: Read từ spreadsheet hoặc HTTP `GET /api/v1/categories/`
3. **Calculate Date Range**: 
   ```js
   const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
   return [{
     json: {
       from_date: today,
       to_date: today,
     }
   }];
   ```
4. **Loop Categories** (Split in Batches): Batch size = 50-100
5. **Loop Pagination** (For Each Category):
   - Start: `page=1`
   - Loop: Call `GET /api/v1/articles/category-date/{category_id}?from_date={{from_date}}&to_date={{to_date}}&page={{page}}&limit=50`
   - Increment `page += 1`
   - Stop khi `offset >= total` (hoặc response.data = empty)
   - **Important**: Thêm delay 100-200ms giữa requests

6. **Code** (Transform):
   ```js
   return items.map((item) => ({
     json: {
       article_id: item.json.id,
       category_id: item.json.category_id || "", // Từ params, không từ response
       title: item.json.title,
       summary: item.json.summary,
       url: item.json.url,
       thumbnail_url: item.json.thumbnail_url || "",
       published_at: "", // Null từ endpoint
       source_endpoint: "category_date",
       page_no: 1,
       date_range: `${$node["Calculate Date Range"].json.from_date}_${$node["Calculate Date Range"].json.to_date}`,
       crawled_at: new Date().toISOString(),
     },
   }));
   ```

7. **Deduplicate** (Optional - nếu rerun):
   - Dedup by `article_id` sử dụng builtin dedup node
   - Hoặc filter bằng SQL ngoài

8. **Spreadsheet**: Append to `articles.xlsx` (mode: APPEND)
9. **Google Drive**: Upload/Update with name `vnexpress_articles_{{$now.toFormat("yyyy-MM-dd_HHmmss")}}.xlsx`

---

### 3.2b Flow: Weekly Backfill (Optional)

**Trigger**: Cron (hàng tuần, Thứ 2 04:00 UTC)

**Steps**:

1. **Trigger - Cron**: `0 4 * * 1`
2. **Calculate Date Range**:
   ```js
   const today = new Date();
   const sevenDaysAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
   return [{
     json: {
       from_date: sevenDaysAgo.toISOString().split('T')[0],
       to_date: today.toISOString().split('T')[0],
     }
   }];
   ```
3. **Loop Categories + Pagination** (như Flow 3.2)
4. **Deduplicate** (bắt buộc vì có overlap với daily)
5. **Spreadsheet**: Append mode
6. **Google Drive**: Upload with name `vnexpress_articles_backfill_{{$now.toFormat("yyyy-MM-dd_HHmmss")}}.xlsx`

---

### 3.3 Flow: Weekly Comments Sync (Optional Phase 2)

**Trigger**: Cron (hàng tuần, Thứ 7 02:00 UTC)

**Steps**:

1. **Trigger - Cron**: `0 2 * * 6`
2. **Read Articles**: Fetch từ recent Excel/DB
3. **Sample Articles**: Lấy top 500 articles (by date hoặc random)
4. **Loop Articles** (Split in Batches): Batch size = 10
5. **Loop Pagination**:
   - Start: `offset=0`
   - Call `GET /api/v1/articles/{id}/comments?object_id={id}&limit=100&sort_by=like&offset={{offset}}`
   - Stop khi hết
6. **Code** (Transform)
7. **Spreadsheet**: Append to `comments.xlsx` (mode: APPEND)
8. **Google Drive**: Upload with name `vnexpress_comments_{{$now.toFormat("yyyy-MM-dd_HHmmss")}}.xlsx`

---

## 4. Lưu ý & Best Practices

### Rate Limiting

- Endpoint không có rate limit công khai
- Recommend: Delay 100-200ms giữa requests
- Max 5-10 concurrent requests

### Data Quality

- **published_at**: Null từ scraping endpoints, có value từ GW API
- **category_id**: Null từ scraping endpoints, có value từ GW API
- **thumbnail_url**: Có thể là placeholder `data:image/gif;base64,...`
- **summary**: Có thể chứa HTML entities, cần decode

### Error Handling

- Retry logic: 3 lần với backoff exponential (1s, 2s, 4s)
- Log error detail: timestamp, endpoint, HTTP status, error message
- Skip failed row, log để manual review

### Incremental Sync

- **Categories**: Full overwrite hàng ngày (nhỏ)
- **Articles**: Append mode (có thể deduplicate by `article_id` ngoài)
- **Comments**: Append mode (có thể sync từng article riêng)

### Performance

- Categories: ~10 phút
- Articles (GW): ~1.5-2 giờ (2366 categories × avg 2-3 articles/category)
- Comments: ~4-6 giờ (1000 articles × avg 20-30 comments/article)

---

## 5. Điểm quyết định

| Câu hỏi              | Đề xuất                              | Thay thế              |
| -------------------- | ------------------------------------ | --------------------- |
| **Articles source**  | GW API                               | Scraping + date range |
| **Excel format**     | 3 sheets trong 1 file                | 3 file riêng          |
| **Comments phase**   | Phase 2 (tuần 2)                     | Phase 1               |
| **Upload frequency** | Daily (categories), Daily (articles) | Weekly                |
| **Data retention**   | Keep all versions on Drive           | Delete old versions   |

---

## 6. Mở rộng tương lai

- [ ] Real-time sync (Webhook + incremental)
- [ ] Data visualization dashboard
- [ ] Duplicate detection & dedup
- [ ] Sentiment analysis trên comments
- [ ] Category hierarchy visualization
