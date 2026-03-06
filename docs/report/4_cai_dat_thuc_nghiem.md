# CHƯƠNG 4. CÀI ĐẶT & THỰC NGHIỆM

Chương này trình bày chi tiết quá trình cài đặt, triển khai và thực nghiệm hệ thống truy hồi thông tin tiếng Việt — VnSearch Engine. Nội dung bao gồm: mô tả môi trường và công cụ phát triển, thiết kế giao diện người dùng, các kịch bản thực nghiệm với kết quả demo thực tế, và đánh giá hiệu năng tổng thể của hệ thống. Toàn bộ hệ thống được đóng gói bằng Docker Compose theo kiến trúc Microservices, cho phép triển khai nhất quán trên mọi môi trường.

---

## 4.1. Môi trường và Công cụ phát triển

### 4.1.1. Ngôn ngữ lập trình

Hệ thống VnSearch Engine được xây dựng trên hai ngôn ngữ lập trình chính, mỗi ngôn ngữ phục vụ cho một nhóm thành phần khác nhau trong kiến trúc Microservices.

**Thứ nhất, Python (phiên bản ≥ 3.12)** được sử dụng cho toàn bộ phần backend, bao gồm IRS API (Backend xử lý NLP và tìm kiếm) và VnExpress Crawler (thu thập dữ liệu). Python được lựa chọn vì hệ sinh thái thư viện phong phú trong lĩnh vực Xử lý Ngôn ngữ Tự nhiên và Học máy (Machine Learning), khả năng xử lý dữ liệu mạnh mẽ với Pandas và NumPy, cùng cộng đồng phát triển lớn hỗ trợ xử lý tiếng Việt [17]. Ngoài ra, Python tích hợp tốt với các công cụ quản lý gói hiện đại như `uv` — trình quản lý gói và môi trường ảo tốc độ cao viết bằng Rust, thay thế cho `pip` và `virtualenv` truyền thống.

**Thứ hai, TypeScript (phiên bản ≥ 5.0)** được sử dụng cho phần Frontend — ứng dụng web IRS Web. TypeScript được lựa chọn thay vì JavaScript thuần nhờ hệ thống kiểu tĩnh (static type system) giúp phát hiện lỗi tại thời điểm biên dịch, cải thiện khả năng bảo trì mã nguồn và hỗ trợ tốt hơn cho các IDE hiện đại trong việc gợi ý và tự hoàn thành mã (autocompletion) [18].

### 4.1.2. Các framework và thư viện chính

#### Backend — IRS API

Bảng 4.1 liệt kê các framework và thư viện chính được sử dụng trong thành phần IRS API:

| **Thư viện**      | **Phiên bản** | **Vai trò**                                                                            |
| ----------------- | ------------- | -------------------------------------------------------------------------------------- |
| FastAPI           | ≥ 0.129.0     | Web framework hiệu suất cao, hỗ trợ async, tự động sinh tài liệu API (Swagger/OpenAPI) |
| Scikit-learn      | ≥ 1.8.0       | Cung cấp `TfidfVectorizer` cho vector hóa văn bản theo sơ đồ TF-IDF [15]               |
| Underthesea       | ≥ 9.2.11      | Thư viện NLP cho tiếng Việt, cung cấp chức năng tách từ (`word_tokenize`) [12]         |
| Pandas            | ≥ 3.0.0       | Thư viện phân tích và xử lý dữ liệu dạng bảng (DataFrame)                              |
| NumPy             | ≥ 2.4.2       | Thư viện tính toán số học, hỗ trợ các phép toán trên mảng và vector                    |
| qdrant-client     | ≥ 1.16.2      | Client Python kết nối và tương tác với cơ sở dữ liệu vector Qdrant [16]                |
| Pydantic Settings | ≥ 2.13.0      | Quản lý cấu hình ứng dụng từ biến môi trường (environment variables)                   |
| Uvicorn           | ≥ 0.40.0      | ASGI server hiệu suất cao dùng để chạy ứng dụng FastAPI                                |
| openpyxl          | ≥ 3.1.5       | Đọc và ghi file Excel (.xlsx), phục vụ nạp dữ liệu đầu vào                             |

_Bảng 4.1. Các thư viện chính của IRS API Backend_

#### Backend — VnExpress Crawler

Bảng 4.2 liệt kê các thư viện chính của thành phần Crawler:

| **Thư viện**   | **Vai trò**                                                                     |
| -------------- | ------------------------------------------------------------------------------- |
| FastAPI        | Web framework cung cấp API cho các endpoint crawl dữ liệu                       |
| httpx          | HTTP client hỗ trợ async, dùng để gửi request đến VnExpress API                 |
| requests       | HTTP client đồng bộ, sử dụng cho các tác vụ crawl đơn giản                      |
| BeautifulSoup4 | Thư viện phân tích cú pháp HTML (HTML parsing), trích xuất dữ liệu từ trang web |
| Pydantic       | Kiểm tra và xác thực dữ liệu (data validation) với hệ thống kiểu                |
| Uvicorn        | ASGI server chạy ứng dụng Crawler                                               |

_Bảng 4.2. Các thư viện chính của VnExpress Crawler_

#### Frontend — IRS Web

Bảng 4.3 liệt kê các framework và thư viện chính của phần Frontend:

| **Thư viện**           | **Phiên bản** | **Vai trò**                                                                   |
| ---------------------- | ------------- | ----------------------------------------------------------------------------- |
| Next.js                | 16.1.6        | React framework hỗ trợ SSR/SSG, App Router, tối ưu hiệu suất [18]             |
| React                  | 19.2.3        | Thư viện xây dựng giao diện người dùng dạng component                         |
| TailwindCSS            | 4.x           | CSS framework utility-first cho phép styling nhanh và nhất quán               |
| Shadcn UI (Radix)      | 1.4.3         | Bộ UI components có tính tiếp cận cao (accessible), dựa trên Radix Primitives |
| Zustand                | 5.0.11        | Thư viện quản lý trạng thái (state management) nhẹ và linh hoạt               |
| React Query (TanStack) | 5.90.21       | Quản lý trạng thái server-side, caching và đồng bộ dữ liệu từ API             |
| Framer Motion          | 12.34.0       | Thư viện animation cho React, hỗ trợ hiệu ứng chuyển động mượt mà             |
| React Three Fiber      | 9.5.0         | React renderer cho Three.js, tạo hiệu ứng 3D trong Hero section               |
| Axios                  | 1.13.5        | HTTP client gửi request từ Frontend đến Backend API                           |
| Zod                    | 4.3.6         | Schema validation cho form input (truy vấn tìm kiếm)                          |
| React Hook Form        | 7.71.1        | Quản lý form hiệu suất cao, kết hợp với Zod validation                        |

_Bảng 4.3. Các thư viện chính của IRS Web Frontend_

### 4.1.3. Hệ quản trị cơ sở dữ liệu

Hệ thống sử dụng hai loại cơ sở dữ liệu phục vụ cho hai mục đích khác nhau, được tổng hợp trong Bảng 4.4:

| **Cơ sở dữ liệu** | **Phiên bản**   | **Loại**        | **Vai trò**                                                        | **Port** |
| ----------------- | --------------- | --------------- | ------------------------------------------------------------------ | -------- |
| Qdrant            | Latest (Docker) | Vector Database | Lưu trữ vector TF-IDF và thực hiện tìm kiếm tương đồng cosine [16] | 6333     |
| PostgreSQL        | 18              | Relational DB   | Cơ sở dữ liệu hỗ trợ cho n8n Workflow Engine                       | 5432     |

_Bảng 4.4. Các hệ quản trị cơ sở dữ liệu trong hệ thống_

**Qdrant** đóng vai trò cốt lõi trong hệ thống — lưu trữ toàn bộ vector biểu diễn TF-IDF của các bài báo cùng metadata (payload) và cung cấp khả năng tìm kiếm tương đồng cosine với thuật toán HNSW (Hierarchical Navigable Small World), đạt thời gian truy vấn ở mức mili-giây. Mỗi điểm dữ liệu (point) trong Qdrant bao gồm: ID (article_id), vector dạng dense (ví dụ: 3.740 chiều), và payload chứa các trường metadata như tiêu đề, tóm tắt, URL, danh mục, ngày xuất bản và số bình luận.

**PostgreSQL** được triển khai để hỗ trợ n8n Workflow Engine — công cụ tự động hóa pipeline thu thập dữ liệu. PostgreSQL lưu trữ cấu hình workflow, lịch sử thực thi và các metadata nội bộ của n8n.

### 4.1.4. Công cụ triển khai và containerization

Toàn bộ hệ thống được đóng gói và triển khai thông qua **Docker** và **Docker Compose**, đảm bảo tính nhất quán môi trường giữa máy phát triển (development) và máy chủ sản phẩm (production). Bảng 4.5 tổng hợp các container trong hệ thống:

| **Container** | **Image**              | **Port**   | **Tài nguyên**          |
| ------------- | ---------------------- | ---------- | ----------------------- |
| `irs_api`     | Build từ Dockerfile    | 8000       | 1.0–2.0 CPU, 1–2 GB RAM |
| `irs_web`     | Build từ Dockerfile    | 3000       | Mặc định                |
| `qdrant`      | `qdrant/qdrant:latest` | 6333, 6334 | 0.5–1.0 CPU, 1–2 GB RAM |
| `postgres`    | `postgres:18`          | 5432       | Mặc định                |
| `n8n`         | `n8nio/n8n:latest`     | 5678       | Mặc định                |

_Bảng 4.5. Danh sách các container trong Docker Compose_

Tất cả các container được kết nối thông qua mạng Docker chung (`main-network`), cho phép giao tiếp nội bộ giữa các service bằng hostname (ví dụ: `irs_api` gọi Qdrant qua hostname `qdrant:6333`). Cấu hình `restart: unless-stopped` được thiết lập cho các service quan trọng (Qdrant, IRS API) nhằm đảm bảo khả năng tự phục hồi khi xảy ra lỗi. Ngoài ra, cơ chế health check được cấu hình cho Qdrant và IRS API để giám sát trạng thái hoạt động theo chu kỳ 30 giây.

Để khởi động toàn bộ hệ thống, chỉ cần thực thi lệnh:

```bash
cd setup
./start.sh
```

Lệnh này sẽ khởi tạo mạng Docker, kéo các image cần thiết và khởi chạy tất cả 5 container theo thứ tự phụ thuộc (dependency order).

---

## 4.2. Thiết kế giao diện (UI)

Giao diện người dùng của hệ thống VnSearch Engine được xây dựng theo triết lý **Minimalist Search Engine** — tập trung vào trải nghiệm tìm kiếm nhanh, trực quan và hiện đại. Giao diện sử dụng thiết kế đáp ứng (responsive design) với ba breakpoint chính: điện thoại di động (mobile), máy tính bảng (tablet) và máy tính để bàn (desktop), đảm bảo trải nghiệm người dùng nhất quán trên mọi thiết bị.

### 4.2.1. Trang chủ — Hero Section và Thanh tìm kiếm

<!-- [Chèn ảnh chụp màn hình trang chủ tại đây] -->
<!-- Hình 4.1. Giao diện trang chủ VnSearch Engine với Hero Section 3D và thanh tìm kiếm -->

Trang chủ của hệ thống bao gồm hai thành phần chính:

**Thứ nhất, Hero Section với hiệu ứng 3D.** Phần trên cùng của trang hiển thị một hệ thống hạt (particle system) 3D được dựng bằng React Three Fiber và Three.js, tạo hiệu ứng thị giác động (dynamic visual effect) làm nền cho tiêu đề hệ thống. Hiệu ứng này không chỉ mang tính thẩm mỹ mà còn truyền tải thông điệp về tính hiện đại và công nghệ cao của hệ thống tìm kiếm ngữ nghĩa.

**Thứ hai, Thanh tìm kiếm (Search Bar).** Đây là thành phần trung tâm, được đặt ở vị trí nổi bật giữa trang. Thanh tìm kiếm hỗ trợ các tính năng sau: xác thực đầu vào (1–500 ký tự) bằng Zod schema, cơ chế chống gửi liên tục (debounce 300ms), nút xóa nội dung (clear button), bộ đếm ký tự (character counter), chỉ báo trạng thái đang tải (loading indicator) và hỗ trợ phím Enter để gửi truy vấn.

### 4.2.2. Bộ lọc và điều khiển kết quả

<!-- [Chèn ảnh chụp màn hình phần bộ lọc tại đây] -->
<!-- Hình 4.2. Bộ lọc danh mục và điều khiển số lượng kết quả -->

Bên dưới thanh tìm kiếm là **Thanh lọc (Filter Bar)** cho phép người dùng tinh chỉnh kết quả tìm kiếm thông qua hai tham số:

- **Bộ lọc danh mục (Category Filter)**: Lọc kết quả theo một trong 7 danh mục hỗ trợ: Khoa học, Ý kiến, Giáo dục, Sức khỏe, Thời sự, Giải trí, Đời sống, hoặc chọn "Tất cả" để không lọc.
- **Giới hạn kết quả (Limit Control)**: Cho phép chọn số lượng kết quả trả về: 5, 10, 20 hoặc 50 bài viết.

Trên thiết bị di động, bộ lọc được trình bày dưới dạng Sheet drawer (Shadcn component) — trượt từ dưới lên — nhằm tối ưu không gian màn hình.

### 4.2.3. Hiển thị kết quả tìm kiếm

<!-- [Chèn ảnh chụp màn hình danh sách kết quả tại đây] -->
<!-- Hình 4.3. Danh sách kết quả tìm kiếm dạng lưới với Article Card -->

Kết quả tìm kiếm được hiển thị theo bố cục lưới đáp ứng (responsive grid): 1 cột trên di động, 2 cột trên máy tính bảng và 3 cột trên máy tính để bàn. Mỗi kết quả được trình bày dưới dạng **Article Card** bao gồm các thông tin:

- **Nhãn danh mục (Category Badge)**: Hiển thị tên danh mục với mã màu riêng biệt cho từng loại (ví dụ: Xanh dương cho Khoa học, Đỏ cho Thời sự), giúp người dùng nhận diện nhanh lĩnh vực bài viết.
- **Tiêu đề bài viết (Title)**: Tiêu đề đầy đủ của bài báo được hiển thị dạng in đậm.
- **Tóm tắt nội dung (Summary)**: Đoạn tóm tắt ngắn gọn, tối đa 2–3 dòng, giúp người dùng đánh giá mức độ liên quan trước khi mở bài viết gốc.
- **Điểm tương đồng (Score)**: Giá trị cosine similarity dưới dạng phần trăm (ví dụ: 46.5%), cho phép người dùng đánh giá mức độ phù hợp của kết quả.
- **Số bình luận (Comments)**: Hiển thị số lượng bình luận của bài viết.
- **Nút hành động (CTA)**: Liên kết đến bài viết gốc trên VnExpress.

Phần **Results Header** hiển thị thông tin tổng hợp: _"Tìm thấy {N} kết quả cho \"{query}\" ({time}ms)"_, cung cấp phản hồi tức thì về hiệu suất tìm kiếm.

Các hiệu ứng giao diện bao gồm: hiệu ứng xuất hiện (fade in) và trượt lên (slide up) sử dụng Framer Motion khi kết quả được tải, hiệu ứng bóng đổ (shadow) và phóng to nhẹ (scale) khi di chuột qua Article Card.

### 4.2.4. Lịch sử tìm kiếm

<!-- [Chèn ảnh chụp màn hình lịch sử tìm kiếm tại đây] -->
<!-- Hình 4.4. Dropdown lịch sử tìm kiếm gần đây -->

Hệ thống lưu trữ lịch sử các truy vấn đã thực hiện sử dụng Zustand kết hợp cơ chế lưu trữ cục bộ (localStorage persistence). Khi người dùng nhấp vào thanh tìm kiếm, danh sách các từ khóa đã tìm gần đây sẽ hiển thị dưới dạng dropdown, cho phép: nhấp để tìm kiếm lại, xóa từng mục hoặc xóa toàn bộ lịch sử.

### 4.2.5. Các trạng thái giao diện đặc biệt

Giao diện hệ thống xử lý ba trạng thái đặc biệt:

- **Trạng thái đang tải (Loading State)**: Hiển thị các thẻ khung xương (skeleton cards) — 3 đến 5 thẻ giữ chỗ với hiệu ứng nhấp nháy — giúp người dùng nhận biết hệ thống đang xử lý truy vấn.
- **Trạng thái không có kết quả (Empty State)**: Hiển thị thông báo _"Không tìm thấy kết quả"_ kèm gợi ý thay đổi từ khóa hoặc bộ lọc.
- **Trạng thái lỗi (Error State)**: Hiển thị thông báo _"Có lỗi xảy ra"_ kèm nút _"Thử lại"_ cho phép người dùng gửi lại truy vấn.

### 4.2.6. Chế độ Sáng/Tối (Dark/Light Mode)

<!-- [Chèn ảnh chụp màn hình chế độ sáng và tối tại đây] -->
<!-- Hình 4.5. So sánh giao diện ở chế độ sáng (Light) và tối (Dark) -->

Hệ thống hỗ trợ chuyển đổi giữa chế độ sáng (Light Mode) và chế độ tối (Dark Mode) thông qua thư viện `next-themes`. Chế độ tối giảm ánh sáng xanh phát ra từ màn hình, giúp giảm mỏi mắt khi sử dụng trong môi trường ánh sáng yếu. Thiết lập mặc định theo cấu hình hệ điều hành của người dùng (system preference).

---

## 4.3. Kịch bản thực nghiệm & Kết quả Demo

Phần này trình bày các kịch bản thực nghiệm trên hệ thống VnSearch Engine với bộ dữ liệu thực tế gồm **2.232 bài báo** được thu thập từ VnExpress, phân bố trên 7 danh mục chính. Vector TF-IDF có số chiều là **3.740**, được lưu trữ trong Qdrant collection `articles`.

### 4.3.1. Kịch bản 1 — Tìm kiếm theo chủ đề "công nghệ trí tuệ nhân tạo"

<!-- [Chèn ảnh chụp màn hình kết quả tại đây] -->
<!-- Hình 4.6. Kết quả tìm kiếm cho truy vấn "công nghệ trí tuệ nhân tạo" -->

**Truy vấn**: _"công nghệ trí tuệ nhân tạo"_
**Bộ lọc**: Tất cả danh mục, Giới hạn: 10

**Quy trình xử lý nội bộ**: Truy vấn được gửi đến API endpoint `POST /api/v1/search`. Hệ thống thực hiện các bước sau: (1) tách từ tiếng Việt bằng Underthesea: _"công_nghệ trí_tuệ nhân_tạo"_; (2) chuẩn hóa chữ thường; (3) loại bỏ từ dừng; (4) chuyển đổi thành vector TF-IDF bằng mô hình đã huấn luyện; (5) gửi vector đến Qdrant để tìm kiếm top-K kết quả theo Cosine Similarity.

**Kết quả mẫu**:

| **STT** | **Tiêu đề**                                               | **Danh mục** | **Score** |
| ------- | --------------------------------------------------------- | ------------ | --------- |
| 1       | Những chính sách khoa học công nghệ được kỳ vọng năm 2025 | Khoa học     | 46.5%     |
| 2       | Ứng dụng AI trong y tế Việt Nam                           | Sức khỏe     | 38.2%     |
| 3       | Xu hướng công nghệ số trong giáo dục                      | Giáo dục     | 35.7%     |

**Nhận xét**: Hệ thống trả về các bài viết liên quan đến chủ đề công nghệ và trí tuệ nhân tạo từ nhiều danh mục khác nhau, cho thấy khả năng tìm kiếm xuyên danh mục (cross-category search) của mô hình VSM-TF-IDF. Query gốc sau bước tiền xử lý NLP (processed*query) cho thấy các từ ghép tiếng Việt được tách đúng: *"công*nghệ"*, _"trí_tuệ"_, _"nhân_tạo"_.

### 4.3.2. Kịch bản 2 — Tìm kiếm có lọc danh mục

<!-- [Chèn ảnh chụp màn hình kết quả tại đây] -->
<!-- Hình 4.7. Kết quả tìm kiếm với bộ lọc danh mục "Khoa học" -->

**Truy vấn**: _"biến đổi khí hậu"_
**Bộ lọc**: Danh mục = Khoa học, Giới hạn: 5

**Kết quả**: Hệ thống chỉ trả về các bài viết thuộc danh mục "Khoa học" có nội dung liên quan đến biến đổi khí hậu. Tính năng lọc danh mục (category_filter) được thực hiện ở tầng Qdrant thông qua cơ chế lọc payload (payload filtering) — chỉ các điểm dữ liệu có trường `category_name` khớp với giá trị bộ lọc mới được đưa vào phép tính tương đồng, giúp thu hẹp không gian tìm kiếm và cải thiện độ phù hợp của kết quả.

### 4.3.3. Kịch bản 3 — Tìm kiếm với từ khóa ngắn

<!-- [Chèn ảnh chụp màn hình kết quả tại đây] -->
<!-- Hình 4.8. Kết quả tìm kiếm cho truy vấn ngắn "giáo dục" -->

**Truy vấn**: _"giáo dục"_
**Bộ lọc**: Tất cả danh mục, Giới hạn: 10

**Nhận xét**: Truy vấn một từ duy nhất vẫn trả về kết quả có ý nghĩa. Do thuật ngữ _"giáo_dục"_ có giá trị IDF tương đối cao (không phải từ dừng nhưng cũng không quá hiếm), hệ thống trả về các bài viết chứa thuật ngữ này với điểm tương đồng phản ánh mức độ tập trung của nội dung vào chủ đề giáo dục. Kịch bản này minh họa khả năng hoạt động ổn định của hệ thống ngay cả với truy vấn ngắn.

### 4.3.4. Kịch bản 4 — Tìm kiếm với truy vấn dài mang tính ngữ cảnh

<!-- [Chèn ảnh chụp màn hình kết quả tại đây] -->
<!-- Hình 4.9. Kết quả tìm kiếm cho truy vấn dài mang tính ngữ cảnh -->

**Truy vấn**: _"ảnh hưởng của dịch bệnh đến đời sống kinh tế xã hội người dân"_
**Bộ lọc**: Tất cả danh mục, Giới hạn: 10

**Nhận xét**: Truy vấn dài với nhiều thuật ngữ được xử lý hiệu quả nhờ cơ chế TF-IDF. Sau bước tiền xử lý NLP, các từ dừng như _"của"_, _"đến"_ được loại bỏ, các từ ghép như _"dịch_bệnh"_, _"đời_sống"_, _"kinh_tế"_, _"xã_hội"_ được tách đúng, giúp vector truy vấn phản ánh chính xác ngữ nghĩa cốt lõi. Kết quả trả về bao phủ nhiều danh mục (Thời sự, Sức khỏe, Đời sống), cho thấy tính chất đa chiều (multi-faceted) của truy vấn được hệ thống nắm bắt ở mức hợp lý thông qua biểu diễn TF-IDF.

---

## 4.4. Đánh giá hiệu năng

### 4.4.1. Hiệu năng thời gian phản hồi

Bảng 4.6 tổng hợp kết quả đo hiệu năng thời gian phản hồi của các endpoint API chính, thực hiện trên môi trường Docker với cấu hình như mô tả ở mục 4.1:

| **Endpoint**          | **Thời gian phản hồi**        | **Mục tiêu**   | **Đánh giá**      |
| --------------------- | ----------------------------- | -------------- | ----------------- |
| `GET /` (Health)      | < 10ms                        | < 10ms         | ✅ Đạt yêu cầu    |
| `POST /api/v1/search` | 50–300ms (trung bình: ~200ms) | < 500ms        | ✅ Đạt yêu cầu    |
| `POST /api/v1/ingest` | 30–60 giây                    | Không giới hạn | ✅ Chấp nhận được |

_Bảng 4.6. Kết quả đo hiệu năng thời gian phản hồi API_

**Phân tích chi tiết thời gian tìm kiếm**: Thời gian phản hồi trung bình của endpoint tìm kiếm (~200ms) bao gồm các giai đoạn: (1) tiền xử lý NLP (tách từ, loại bỏ từ dừng): ~20–50ms; (2) vector hóa TF-IDF (transform bằng mô hình đã lưu): ~30–80ms; (3) tìm kiếm tương đồng trên Qdrant: ~10–50ms; (4) xây dựng và trả về response: ~5–20ms. Giai đoạn vector hóa chiếm thời gian lớn nhất do cần tải mô hình TF-IDF đã lưu (pickle) và thực hiện phép biến đổi ma trận thưa (sparse matrix transformation). Giai đoạn tìm kiếm trên Qdrant có thời gian rất thấp nhờ thuật toán HNSW được tối ưu cho tìm kiếm láng giềng gần đúng (ANN) [16].

Thời gian phản hồi đạt **dưới 500ms** cho tất cả các truy vấn thử nghiệm, thấp hơn ngưỡng nhận thức "tức thì" của người dùng (thường được xác định ở mức 1 giây) [19], đảm bảo trải nghiệm tìm kiếm mượt mà.

### 4.4.2. Hiệu năng Frontend

Bảng 4.7 trình bày các chỉ số hiệu năng Frontend mục tiêu và kết quả thực tế:

| **Chỉ số**               | **Mục tiêu** | **Kết quả thực tế** | **Đánh giá**   |
| ------------------------ | ------------ | ------------------- | -------------- |
| First Load (lần tải đầu) | < 1 giây     | < 1 giây            | ✅ Đạt yêu cầu |
| Thời gian tìm kiếm E2E   | < 500ms      | ~200–400ms          | ✅ Đạt yêu cầu |
| Hiệu ứng animation       | 60fps        | 60fps               | ✅ Đạt yêu cầu |

_Bảng 4.7. Các chỉ số hiệu năng Frontend_

Giao diện Next.js tận dụng cơ chế Server-Side Rendering (SSR) và tối ưu hóa bundle size để đạt thời gian tải đầu tiên nhanh. React Query caching đảm bảo rằng các truy vấn trùng lặp không phải gọi lại API, cải thiện đáng kể trải nghiệm khi người dùng quay lại các từ khóa đã tìm trước đó.

### 4.4.3. Đánh giá độ chính xác kết quả tìm kiếm

Như đã trình bày ở mục 1.3.2, đề tài chưa có bộ dữ liệu benchmark chuẩn (ground truth) cho bài toán truy hồi thông tin tiếng Việt trên dữ liệu tin tức, do đó đánh giá độ chính xác được thực hiện ở mức **định tính** (qualitative evaluation) thông qua kiểm tra thủ công.

**Các quan sát chính:**

**Thứ nhất**, về khả năng tìm kiếm ngữ nghĩa cơ bản: hệ thống trả về kết quả liên quan cho phần lớn các truy vấn thử nghiệm. Các bài viết có điểm tương đồng cosine cao (≥ 0.3) thường có nội dung liên quan trực tiếp đến chủ đề truy vấn. Điều này xác nhận tính hiệu quả của sơ đồ trọng số TF-IDF trong việc nắm bắt các đặc trưng từ vựng (lexical features) của văn bản tiếng Việt.

**Thứ hai**, về vai trò của bước tiền xử lý NLP: chất lượng tách từ tiếng Việt của Underthesea ảnh hưởng trực tiếp đến kết quả. Khi các từ ghép được tách đúng (ví dụ: _"trí_tuệ_nhân_tạo"_ thay vì _"trí"_, _"tuệ"_, _"nhân"_, _"tạo"_), vector biểu diễn phản ánh chính xác ngữ nghĩa, dẫn đến kết quả truy hồi chất lượng hơn.

**Thứ ba**, về hạn chế của TF-IDF: mô hình TF-IDF không xử lý được các trường hợp đồng nghĩa (synonymy). Ví dụ, truy vấn _"AI"_ sẽ không tìm được bài viết chỉ chứa _"trí tuệ nhân tạo"_ mà không có từ _"AI"_, vì TF-IDF hoạt động dựa trên khớp từ vựng (lexical matching) chứ không phải khớp ngữ nghĩa sâu (deep semantic matching). Đây là hạn chế mang tính bản chất của phương pháp biểu diễn thưa (sparse representation) đã được nhận thức ở giai đoạn thiết kế (mục 1.3.2).

### 4.4.4. Tổng hợp đánh giá

Bảng 4.8 tổng hợp đánh giá toàn diện hiệu năng hệ thống:

| **Tiêu chí**               | **Kết quả**                              | **Đánh giá** |
| -------------------------- | ---------------------------------------- | ------------ |
| Thời gian phản hồi API     | < 500ms (trung bình ~200ms)              | Tốt          |
| Thời gian tìm kiếm vector  | < 50ms                                   | Rất tốt      |
| Tìm kiếm xuyên danh mục    | Hoạt động chính xác                      | Tốt          |
| Lọc theo danh mục          | Hoạt động chính xác                      | Tốt          |
| Xử lý truy vấn ngắn (1 từ) | Trả về kết quả hợp lý                    | Khá          |
| Xử lý truy vấn dài         | Trả về kết quả đa chiều, phong phú       | Tốt          |
| Tách từ tiếng Việt         | Chính xác với phần lớn trường hợp        | Tốt          |
| Giao diện responsive       | Hoạt động tốt trên mobile/tablet/desktop | Tốt          |
| Khả năng triển khai Docker | Một lệnh khởi động toàn bộ hệ thống      | Rất tốt      |

_Bảng 4.8. Tổng hợp đánh giá hiệu năng hệ thống VnSearch Engine_

Tóm lại, hệ thống VnSearch Engine đáp ứng tốt các yêu cầu về hiệu năng thời gian phản hồi (< 500ms) và khả năng triển khai (Docker Compose). Kết quả tìm kiếm cho thấy tính khả thi của phương pháp VSM kết hợp TF-IDF trong bài toán truy hồi thông tin tiếng Việt. Các hạn chế chính — bao gồm khả năng nắm bắt ngữ nghĩa sâu và xử lý đồng nghĩa — là đặc trưng mang tính bản chất của sơ đồ trọng số TF-IDF và có thể được cải thiện bằng các phương pháp nhúng ngữ nghĩa sâu (dense embedding) trong hướng phát triển tương lai.

---

## Tài liệu tham khảo Chương 4

[17] G. van Rossum, "Python Tutorial," _Python Software Foundation_, 2024. [Trực tuyến]. Truy cập: https://docs.python.org/3/tutorial/

[18] Vercel, "Next.js Documentation," _Vercel_, 2024. [Trực tuyến]. Truy cập: https://nextjs.org/docs

[19] J. Nielsen, _Usability Engineering_, Academic Press, 1993.

> **Ghi chú**: Tài liệu [12] (Underthesea — Vu, 2017), [15] (Scikit-learn — Pedregosa et al., 2011) và [16] (Qdrant Documentation) đã được giới thiệu ở Chương 2 và được trích dẫn lại ở Chương 4 với cùng số thứ tự để đảm bảo tính nhất quán.
