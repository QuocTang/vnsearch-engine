# VnExpress API Research

## Domain Analysis

### APIs Discovered

#### 1. **Category API** ✅ Working
- **Endpoint**: `https://vnexpress.net/microservice/fc`
- **Description**: Fetch all VnExpress categories with hierarchy
- **Response**: Dictionary of category objects with id, url, name, parent_id
- **Status**: Fully accessible, no authentication required

#### 2. **Comments API** ✅ Working
- **Endpoint**: `https://usi-saas.vnexpress.net/index/get`
- **Parameters**:
  - `offset`: Pagination offset
  - `limit`: Number of comments (default 20)
  - `objectid`: Article object ID (required)
  - `objecttype`: Type (1=article)
  - `sort_by`: Sort order (like, newest, oldest)
  - `siteid`: Site ID (1000000)
- **Response**: Comments with author, content, creation time, likes count
- **Status**: Fully accessible, no authentication required
- **Example**:
  ```
  https://usi-saas.vnexpress.net/index/get?offset=0&limit=20&objectid=4988419&objecttype=1&sort_by=like
  ```

#### 3. **Article API** ✅ **FOUND** (GW API)
- **Endpoint**: `https://gw.vnexpress.net/bt`
- **Status**: Fully accessible, provides article data for all categories
- **Parameters**:
  - `site_id`: Site ID (1000000)
  - `category_id`: Category ID
  - `showed_area`: Content area selector (e.g., `doanhnghiep:20`)
  - `limit`: Number of articles
  - `data_select`: Fields to return (article_id, title, share_url, thumbnail_url, publish_time, lead)
- **Response**: JSON with article metadata
- **Example**:
  ```
  https://gw.vnexpress.net/bt?site_id=1000000&category_id=1000000&showed_area=doanhnghiep:20&limit=20&data_select=article_id,title,share_url,thumbnail_url,publish_time,lead
  ```
- **Note**: The `showed_area` parameter varies by category. The value before colon (e.g., `doanhnghiep`) is the content section name.

---

## Data Available

### Categories
- 2366 categories available
- Hierarchy support (parent-child relationships)
- URL slugs for each category
- Example: Category 1001005 = "Thời sự" (Current Affairs)

### Comments
- Can fetch up to 100 comments per request
- Sorted by likes, newest, or oldest
- Author information included
- Like counts available
- Timestamps included
- Nested replies supported (in API response)

### Articles
- No direct API available
- Would require browser automation or web scraping

---

## Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Categories | ✅ Done | Fully working with caching |
| Category Search | ✅ Done | By name matching |
| Comments | ✅ Done | By article object ID |
| Articles | ✅ Done | Via GW API endpoint - Fast & reliable |

---

## Opportunities for Enhancement

### 1. **Article Extraction**
Could be implemented using:
- Selenium / Playwright (browser automation)
- BeautifulSoup (web scraping)
- Requires user-agent and proper headers

### 2. **Comment Metadata**
Currently available and extractable:
- Reaction types (funny, sad, angry, etc.)
- User IDs and types
- Comment threading/replies
- Is pinned status

### 3. **Real-time Updates**
- Comments API supports sorting by "newest"
- Can be polled for real-time comment streams

### 4. **User Profiles**
- User IDs available in comments
- Could potentially fetch user data via separate API

### 5. **Trending Articles**
- Could rank articles by comment counts
- Could analyze comment sentiment
- Could track trending topics by category

---

## Findings

1. **VnExpress uses a microservices architecture** - Categories on `/microservice/fc`, Comments on `usi-saas.vnexpress.net`

2. **Client-side rendering** - Articles are rendered via JavaScript, not available via API

3. **Comments are the most accessible data** - Can extract author, content, engagement metrics

4. **No authentication required** - All endpoints are publicly accessible

5. **Rate limiting** - None observed during testing, but may be implemented

---

## Recommendations

1. ✅ **Current Implementation**: Focus on categories and comments (already implemented)

2. 🔄 **Future Enhancement**: Add comment aggregation and sentiment analysis

3. 📊 **Analytics**: Create trending topics endpoint based on comment volume

4. 🤖 **Article Scraping**: If articles are needed, implement Playwright for browser automation

5. 📱 **User Engagement**: Track author activity and high-engagement comments
