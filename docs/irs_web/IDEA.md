# IRS Web - Ý tưởng UI/UX và Tính năng

**Dựa trên**: IRS API v1.0.0  
**Mục tiêu**: Web app tìm kiếm semantic articles tiếng Việt

---

## 🎨 Bức tranh tổng quan

### Concept

**Minimalist Search Engine** - Tập trung vào trải nghiệm tìm kiếm nhanh, trực quan với kết quả relevant cao.

### Design Philosophy

- **Clean & Simple**: Giao diện tối giản, không phức tạp
- **Fast**: Phản hồi nhanh với loading states rõ ràng
- **Vietnamese-first**: Tối ưu cho tiếng Việt
- **Mobile-friendly**: Responsive trên mọi thiết bị

### UI Structure

```
┌─────────────────────────────────────┐
│           Header (Logo + Nav)        │
├─────────────────────────────────────┤
│                                      │
│         Search Bar (Center)          │
│                                      │
├─────────────────────────────────────┤
│                                      │
│         Search Results               │
│         (Article Cards)              │
│                                      │
└─────────────────────────────────────┘
```

---

## 🎯 Core Features

### 1. Search Bar (Main Feature)

**Vị trí**: Center - Hero section

**Components**:

- Input field lớn, thu hút attention
- Search button hoặc Enter to search
- Placeholder: "Tìm kiếm bài viết..." hoặc dynamic examples
- Character counter: "0/500" (validation feedback)

**Features**:

- ✅ Real-time validation
- ✅ Debounced search (300ms sau khi user ngừng typing)
- ✅ Clear button (×) khi có text
- ✅ Loading indicator khi đang search
- ✅ Enter key support

**States**:

- Empty (placeholder visible)
- Typing (show character count)
- Loading (spinner in button)
- Error (red border + message)

---

### 2. Filter Bar (Optional - phía trên results)

**Vị trí**: Dưới search bar, trên results

**Components**:

- **Category Dropdown/Tags**:
  - "Tất cả" (default)
  - "Khoa học", "Ý kiến", "Giáo dục", "Sức khỏe", "Thời sự", "Giải trí", "Đời sống"
- **Results Limit Slider**: 5, 10, 20, 50
- **Applied filters tags** (removable)

**Features**:

- ✅ Click category để filter
- ✅ Multi-select categories (hoặc single-select)
- ✅ Clear all filters button
- ✅ Filter count badge: "2 filters applied"

---

### 3. Search Results

**Vị trí**: Main content area

**Layout**: Vertical list hoặc Grid (2-3 columns trên desktop)

**Article Card Design**:

```
┌─────────────────────────────────────────┐
│ [Category Badge]           [Score: 85%] │
│ Title (h3, 2 lines max)                 │
│ Summary (p, 3-4 lines)                  │
│                                          │
│ 📝 12 comments  |  🕐 2 hours ago       │
│ [Đọc thêm →]                            │
└─────────────────────────────────────────┘
```

**Card Components**:

- **Category Badge**: Màu riêng cho từng category
- **Relevance Score**: Hiển thị % (score × 100)
- **Title**: Bold, clickable
- **Summary**: 3-4 dòng, text-overflow ellipsis
- **Metadata**: Comments count, timestamp (nếu có)
- **CTA Button**: "Đọc thêm" link to article URL

**Features**:

- ✅ Hover effect (shadow, scale)
- ✅ Click card → open article (new tab)
- ✅ Lazy loading (infinite scroll hoặc pagination)
- ✅ Empty state: "Không tìm thấy kết quả"

---

### 4. Results Header

**Vị trí**: Trên danh sách results

**Display**:

```
Tìm thấy 15 kết quả cho "công nghệ AI" (243ms)
```

**Components**:

- Results count
- Query hiển thị (highlight)
- Execution time
- Sort options (optional): Relevance, Date, Comments

---

### 5. Loading & Empty States

**Loading State**:

- Skeleton cards (3-5 cards)
- Hoặc spinner với text "Đang tìm kiếm..."

**Empty State**:

```
🔍 Không tìm thấy kết quả

Gợi ý:
- Thử từ khóa khác
- Kiểm tra chính tả
- Giảm số lượng filters
```

**Error State**:

```
⚠️ Có lỗi xảy ra

API không phản hồi. Vui lòng thử lại.
[Thử lại]
```

---

### 6. Header

**Components**:

- **Logo**: "IRS Search" hoặc custom logo
- **Navigation** (optional):
  - Home
  - About
  - API Docs (link to /docs)
- **Status Indicator**: Green dot nếu API healthy

**Features**:

- Sticky header khi scroll
- Mobile: Hamburger menu

---

### 7. Footer (Optional)

**Components**:

- Copyright / Credits
- Links: Privacy, Terms, Contact
- Tech stack: "Powered by FastAPI + Qdrant"

---

## 🔄 User Flows

### Flow 1: Simple Search

```
User lands on page
  → Sees empty search bar (hero)
    → Types query: "công nghệ AI"
      → Debounce 300ms
        → API call
          → Loading state (skeleton cards)
            → Results displayed (2 articles)
              → User clicks card
                → Opens article in new tab
```

### Flow 2: Filter Search

```
User searches "giáo dục"
  → Results shown (20 results)
    → User clicks Category filter: "Khoa học"
      → API call with category_filter
        → Filtered results (5 results)
          → User removes filter
            → Back to 20 results
```

### Flow 3: Error Handling

```
User searches
  → API down (500 error)
    → Error message displayed
      → User clicks "Thử lại"
        → Retry API call
```

---

## 🧩 Component Breakdown

### Priority 1 (MVP)

1. **SearchBar** - Input + button + validation
2. **SearchResults** - List of ArticleCard
3. **ArticleCard** - Single result item
4. **LoadingState** - Skeleton or spinner
5. **EmptyState** - No results message

### Priority 2 (Enhanced)

6. **FilterBar** - Category filter + limit
7. **ResultsHeader** - Count + execution time
8. **Header** - Logo + nav + status
9. **ErrorBoundary** - Error handling

### Priority 3 (Polish)

10. **Footer** - Credits + links
11. **ScrollToTop** - Button khi scroll xuống
12. **SearchHistory** - Recent searches (localStorage)
13. **SearchSuggestions** - Popular queries

---

## 📱 Responsive Breakpoints

```
Mobile: < 640px (1 column)
Tablet: 640-1024px (2 columns)
Desktop: > 1024px (3 columns hoặc wide list)
```

**Mobile-first approach**:

- Search bar full width
- Filters: Accordion/Drawer
- Results: Single column
- Cards: Compact layout

---

## ⚡ Performance Requirements

1. **First Load**: < 1s
2. **Search Response**: < 500ms (API ~200ms + render)
3. **Smooth Animations**: 60fps
4. **Lighthouse Score**: > 90

---

## 🔧 Technical Stack (Suggestions)

```
- TailwindCSS
- Nextjs
- Axios
- Threejs
- Shadcn/ui
- React Query (caching)
- Zustand
- React Hook Form
```

---

## 📦 Features Roadmap

### Phase 1: MVP (Week 1)

- [ ] Search bar với validation
- [ ] Search results display
- [ ] Article cards
- [ ] Loading & empty states
- [ ] Basic error handling

### Phase 2: Enhanced (Week 2)

- [ ] Category filter
- [ ] Results limit control
- [ ] Header với status indicator
- [ ] Mobile responsive
- [ ] Debounced search

### Phase 3: Polish (Week 3)

- [ ] Search history (localStorage)
- [ ] Scroll to top button
- [ ] Footer
- [ ] Animations & transitions
- [ ] Accessibility (a11y)

### Phase 4: Advanced (Future)

- [ ] Dark mode toggle
- [ ] Search suggestions/autocomplete
- [ ] Bookmark articles (localStorage)
- [ ] Share results (URL params)
- [ ] Analytics tracking

---

## 🎯 Success Metrics

**User Experience**:

- ✅ User có thể search trong < 3 clicks
- ✅ Results hiển thị trong < 1 second
- ✅ 0 javascript errors
- ✅ Mobile usable (thumb-friendly)

**Technical**:

- ✅ 100% API coverage
- ✅ Error handling for all states
- ✅ Responsive all sizes
- ✅ Accessible (WCAG AA)

---

## 🖼️ Wireframe Concept (Text)

```
┌────────────────────────────────────────────────┐
│  🔍 IRS Search             [Status: 🟢 Online] │
├────────────────────────────────────────────────┤
│                                                 │
│                                                 │
│         ╔════════════════════════════╗         │
│         ║  Tìm kiếm bài viết...     ║  [🔍]    │
│         ╚════════════════════════════╝         │
│                  0/500 characters               │
│                                                 │
├────────────────────────────────────────────────┤
│  [Tất cả ▾]  [Limit: 10 ▾]          Sort by ▾ │
├────────────────────────────────────────────────┤
│  Tìm thấy 15 kết quả (243ms)                   │
├────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────┐  │
│  │ [Khoa học]                      Score:85%│  │
│  │ Những chính sách khoa học...             │  │
│  │ Năm 2025, Chính phủ xác định ưu tiên... │  │
│  │ 📝 1 comments                             │  │
│  │ [Đọc thêm →]                             │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
│  ┌─────────────────────────────────────────┐  │
│  │ [Ý kiến]                        Score:75%│  │
│  │ Trái đắng kiếm sống...                   │  │
│  │ Cứ nghĩ chạy xe ôm công nghệ dễ...       │  │
│  │ 📝 36 comments                            │  │
│  │ [Đọc thêm →]                             │  │
│  └─────────────────────────────────────────┘  │
│                                                 │
└────────────────────────────────────────────────┘
```

---

**Created**: 2026-02-16  
**For**: IRS Web Frontend  
**Based on**: IRS API v1.0.0
