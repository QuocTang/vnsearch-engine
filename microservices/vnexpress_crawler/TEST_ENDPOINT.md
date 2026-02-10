# VnExpress Crawler API - Test Report

**Date**: 2025-12-09  
**Status**: 11/11 passed (100%) - All endpoints working!

---

## Test Summary

| # | Endpoint | Method | Status | Data | Result |
|---|----------|--------|--------|------|--------|
| 1 | `/health` | GET | 200 | ✓ | ✅ PASS |
| 2 | `/api/v1/categories/` | GET | 200 | ✓ | ✅ PASS |
| 3 | `/api/v1/categories/{id}` | GET | 200 | ✓ | ✅ PASS |
| 4 | `/api/v1/categories/search` | GET | 200 | ✓ | ✅ PASS |
| 5 | `/api/v1/articles/category/{id}` | GET | 200 | ✓ | ✅ PASS |
| 6 | `/api/v1/articles/category-paginated/{url}` | GET | 200 | ✓ | ✅ PASS |
| 7 | `/api/v1/articles/category-date/{id}` | GET | 200 | ✓ | ✅ PASS |
| 8 | `/api/v1/articles/{id}/comments` | GET | 200 | ✓ | ✅ PASS |
| 9 | `/openapi.json` | GET | 200 | ✓ | ✅ PASS |
| 10 | `/docs` | GET | 200 | ✓ | ✅ PASS |
| 11 | `/redoc` | GET | 200 | ✓ | ✅ PASS |

---

## Detailed Results

### ✅ Working Endpoints (All Verified)

1. **Health Check** - `/health`
   - Status: 200 ✅
   - Returns: API version, status, timestamp
   - **Test**: `curl http://localhost:8000/health | jq`

2. **Get All Categories** - `/api/v1/categories/`
   - Status: 200 ✅
   - Returns: 2366 total categories with metadata
   - **Test**: `curl http://localhost:8000/api/v1/categories/ | jq '.data | keys[0:5]'`

3. **Get Specific Category** - `/api/v1/categories/{id}`
   - Status: 200 ✅
   - Returns: Category "Thời sự" (Current Affairs)
   - **Response fields**:
     - `id`: Category ID
     - `url`: Category URL slug (e.g., `/thoi-su`)
     - `name`: Category name (e.g., `Thời sự`)
     - `parent_id`: Parent category ID (if any)
   - **Test**: `curl http://localhost:8000/api/v1/categories/1001005 | jq`
   - **Example IDs**: 1001005, 1001002, 1001006, 1001007, 1001009

4. **Search Categories** - `/api/v1/categories/search?q={query}`
   - Status: 200 ✅
   - Returns: 5 matching results
   - **Test**: `curl 'http://localhost:8000/api/v1/categories/search?q=the' | jq '.data[0:2]'`
   - **Try**: `q=khoa`, `q=the`, `q=phap`, `q=sport`

5. **Articles by Category** - `/api/v1/articles/category/{id}?limit={limit}&offset={offset}`
   - Status: 200 ✅
   - Returns: 5 articles with real data
   - Sample: "Giảm bụi mịn PM2.5 với giải pháp lọc không khí chủ động"
   - Data: ✓ Real articles from VnExpress GW API
   - Method: Direct API call to `gw.vnexpress.net/bt`
   - Includes: title, URL, summary, thumbnail, published_at, category_id
   - **Test**: `curl 'http://localhost:8000/api/v1/articles/category/1000000?limit=5' | jq '.data[0:2]'`
   - **Try**: 
     - `category_id=1000000` (all news)
     - `limit=10&offset=0` (pagination)
     - `limit=20&offset=20` (next page)

6. **Articles by Category (Paginated)** - `/api/v1/articles/category-paginated/{category_url}?page={page}&limit={limit}`
    - Status: 200 ✅
    - Returns: Articles with real pagination via web scraping
    - Method: HTML scraping with pagination support (p2, p3, etc)
    - Includes: title, URL, summary, thumbnail, published_at
    - **Test**: `curl 'http://localhost:8000/api/v1/articles/category-paginated/the-gioi?page=1&limit=20' | jq '.data[0:2]'`
    - **Try**:
      - `page=1&limit=20` (first page)
      - `page=2&limit=20` (second page)
      - `category_url=thoi-su` (different category)
      - `category_url=the-gioi` (world news)

7. **Articles by Category & Date Range** - `/api/v1/articles/category-date/{category_id}?from_date={YYYY-MM-DD}&to_date={YYYY-MM-DD}&page={page}&limit={limit}`
    - Status: 200 ✅
    - Returns: Articles within date range with pagination
    - Method: HTML scraping by date filter
    - **Test**: `curl 'http://localhost:8000/api/v1/articles/category-date/1001002?from_date=2025-09-01&to_date=2025-12-09&page=1&limit=10' | jq '.total, .offset, .data[0:2]'`
    - **Try**:
      - `category_id=1001002&from_date=2025-09-01&to_date=2025-12-09&page=1` (Thế giới, page 1)
      - `category_id=1001002&from_date=2025-09-01&to_date=2025-12-09&page=2&limit=10` (page 2)
      - `category_id=1001005&from_date=2025-08-01&to_date=2025-08-31` (Thời sự - 1 month)

8. **Article Comments** - `/api/v1/articles/{id}/comments?object_id={object_id}&limit={limit}&sort_by={sort}`
   - Status: 200 ✅
   - Returns: 20 comments (total), showing first 2
   - Sample author: "Vu Lam"
   - Data: ✓ Real data from VnExpress Comment API
   - Includes: author, content, created_at, likes count
   - API endpoint: `usi-saas.vnexpress.net/index/get`
   - **Test**: `curl 'http://localhost:8000/api/v1/articles/4988419/comments?object_id=4988419&limit=5' | jq '.data[0:2]'`
   - **Try**:
     - `sort_by=like` (default - sorted by likes)
     - `sort_by=newest` (newest first)
     - `sort_by=oldest` (oldest first)
     - `limit=10&offset=0` (pagination)

9. **Documentation - Swagger** - `/docs`
   - Status: 200 ✅
   - Auto-generated interactive Swagger UI
   - **Visit**: `http://localhost:8000/docs`

10. **Documentation - ReDoc** - `/redoc`
   - Status: 200 ✅
   - Auto-generated ReDoc documentation
   - **Visit**: `http://localhost:8000/redoc`

11. **OpenAPI Schema** - `/openapi.json`
   - Status: 200 ✅
   - Machine-readable OpenAPI 3.0 specification
   - **Test**: `curl http://localhost:8000/openapi.json | jq '.info'`

---

## Conclusion

**All 11 endpoints working (100%)**:

✅ **Fully Functional**:
- Health check
- Categories (list, get, search with caching)
- Articles by category (via GW API - Fast!)
- Articles with pagination (web scraping - real page support)
- Articles by date range (web scraping - temporal filtering)
- Comments with sorting and pagination
- Swagger/OpenAPI documentation

**Key Finding**: 
The problem was that VnExpress has a **hidden GW API** (`gw.vnexpress.net/bt`) that provides direct article access without needing browser automation. This endpoint was discovered through domain research.

**Technologies Used**:
- **Direct API Calls**: Categories, Articles, Comments
- **Web Scraping**: Pagination, Date filtering (BeautifulSoup4)
- **Endpoints**: 
  - `vnexpress.net/microservice/fc` - Categories
  - `gw.vnexpress.net/bt` - Articles (GW API) ⭐
  - `vnexpress.net/category/**` - Articles (Scraping - Pagination/Date)
  - `usi-saas.vnexpress.net/index/get` - Comments
- **Caching**: In-memory with TTL

**Performance**:
- GW API articles: ~500ms (first request)
- Scraped articles: ~1-2s (first request, depends on page size)
- Cached responses: instant
- No browser overhead needed!

See [SCRAPER_SETUP.md](./SCRAPER_SETUP.md) for setup and usage instructions. See [RESEARCH.md](./RESEARCH.md) for detailed domain analysis.
