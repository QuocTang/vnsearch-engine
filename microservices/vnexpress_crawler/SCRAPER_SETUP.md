# Article API Setup

## Installation

The API uses VnExpress GW API endpoint (`gw.vnexpress.net/bt`) to fetch articles - no browser automation needed!

### 1. Install Dependencies
```bash
uv sync
```

### 2. Run the API
```bash
uv run main.py
```

---

## Usage

### Get Articles by Category
```bash
curl "http://localhost:8000/api/v1/articles/category/1000000?limit=20&offset=0"
```

**Example Categories**:
- 1000000: VnExpress (All news)
- 1001005: Thời sự (Current Affairs)
- 1001002: Thế giới (World)
- 1001006: Oto Xe may (Vehicles)
- 1001007: Pháp luật (Law)
- 1001009: Khoa học (Science)
- 1001011: Thư giãn (Entertainment)
- 1001012: Ý kiến (Opinion)

**Parameters**:
- `limit`: Number of articles (default: 20, max: 100)
- `offset`: Pagination offset (default: 0)

**Response**:
```json
{
  "status": "success",
  "total": 20,
  "limit": 20,
  "offset": 0,
  "data": [
    {
      "id": "1001005_0",
      "title": "Article Title",
      "url": "https://vnexpress.net/...",
      "category_id": "1001005"
    }
  ]
}
```

### Get Article Details
```bash
curl "http://localhost:8000/api/v1/articles/url/details?url=https://vnexpress.net/the-gioi/..."
```

**Parameters**:
- `url`: Full VnExpress article URL (required)

**Response**:
```json
{
  "id": null,
  "title": "Article Title",
  "url": "https://vnexpress.net/...",
  "summary": "Article summary/description",
  "thumbnail_url": "https://...",
  "published_at": null,
  "category_id": null
}
```

---

## How It Works

1. **API Call**:
   - Makes direct HTTP request to `gw.vnexpress.net/bt`
   - Sends category ID and parameters
   - Receives JSON with article data

2. **Data Extraction**:
   - Parses JSON response
   - Extracts title, URL, summary, thumbnail from each article
   - Structures as Article objects

3. **Caching**:
   - Results cached in memory for `CACHE_ARTICLES` seconds (default 300s)
   - Reduces API calls and improves response time

---

## Performance Notes

- **First request**: ~500ms (API call)
- **Subsequent requests within cache TTL**: instant (in-memory)
- **No browser overhead** - Direct API calls are fast
- **Scalable** - Can handle many concurrent requests

---

## API Response Format

```json
{
  "status": "success",
  "total": 20,
  "limit": 20,
  "offset": 0,
  "data": [
    {
      "id": "4991207",
      "title": "Giảm bụi mịn PM2.5 với giải pháp lọc không khí chủ động",
      "url": "https://vnexpress.net/giam-bui-min-pm2-5-voi-giai-phap-loc-khong-khi-chu-dong-4991207.html",
      "summary": "Ô nhiễm bụi mịn liên tục tăng...",
      "thumbnail_url": "https://i-kinhdoanh.vnecdn.net/...",
      "published_at": 1765288800,
      "category_id": "1000000"
    }
  ]
}
```

---

## Troubleshooting

### Empty results
- Check if category_id is valid
- Verify internet connection to VnExpress API
- Check logs for error details

### Rate limiting
- VnExpress may rate limit requests
- Use cache TTL to reduce requests
- Add delays between requests if needed

---

## Future Improvements

- [ ] Support filtering by date range
- [ ] Add sorting options
- [ ] Monitor API availability
- [ ] Implement automatic retry on failure
- [ ] Support more article metadata
