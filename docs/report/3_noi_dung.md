# CHƯƠNG 3. NỘI DUNG TIỂU LUẬN (CÁCH TIẾP CẬN VÀ PHƯƠNG PHÁP XÂY DỰNG)

Chương này mô tả chi tiết cách tiếp cận và các bước xây dựng hệ thống truy hồi thông tin ngữ nghĩa tiếng Việt — VnSearch Engine. Nội dung bao gồm: kiến trúc tổng thể với sơ đồ luồng hoạt động, quy trình thu thập và tiền xử lý dữ liệu, phương pháp xây dựng mô hình biểu diễn TF-IDF, cơ chế lưu trữ và quản lý chỉ mục trên cơ sở dữ liệu vector Qdrant, và quy trình xử lý truy vấn tìm kiếm ngữ nghĩa. Mỗi thành phần được trình bày kèm theo thiết kế chi tiết và cách áp dụng cụ thể trong mã nguồn của hệ thống.

---

## 3.1. Kiến trúc tổng thể của hệ thống

### 3.1.1. Mô hình kiến trúc Microservices

Hệ thống VnSearch Engine được thiết kế theo kiến trúc Microservices (vi dịch vụ), trong đó mỗi thành phần chức năng được tách thành một dịch vụ độc lập, giao tiếp thông qua giao thức HTTP/REST. Kiến trúc Microservices được lựa chọn vì khả năng phát triển, triển khai và mở rộng từng thành phần một cách độc lập, giảm thiểu sự phụ thuộc lẫn nhau giữa các module [20]. Toàn bộ các dịch vụ được đóng gói và điều phối bằng Docker Compose, đảm bảo tính nhất quán giữa môi trường phát triển và triển khai sản xuất.

Hệ thống bao gồm năm dịch vụ chính, được phân chia theo chức năng thành ba nhóm: nhóm hệ thống lõi (Core System), nhóm đường ống dữ liệu (Data Pipeline) và nhóm lưu trữ dữ liệu (Data Storage). Bảng 3.1 tóm tắt các dịch vụ và vai trò tương ứng:

| **Dịch vụ**         | **Công nghệ**                | **Cổng** | **Vai trò**                                            |
| -------------------- | ---------------------------- | -------- | ------------------------------------------------------ |
| IRS API (Backend)    | FastAPI, Scikit-learn        | 8000     | Xử lý NLP, vector hóa TF-IDF, phục vụ API tìm kiếm   |
| IRS Web (Frontend)   | Next.js 16, React 19         | 3000     | Giao diện tìm kiếm cho người dùng                      |
| Qdrant               | Qdrant Vector DB             | 6333     | Lưu trữ vector và tìm kiếm tương đồng cosine           |
| VnExpress Crawler    | FastAPI (Python)             | 8001     | Thu thập dữ liệu bài báo từ VnExpress                  |
| n8n + PostgreSQL     | n8n, PostgreSQL 18           | 5678     | Tự động hóa pipeline thu thập dữ liệu                  |

_Bảng 3.1. Tổng hợp các dịch vụ trong hệ thống VnSearch Engine_

### 3.1.2. Sơ đồ luồng hoạt động tổng thể

Hệ thống VnSearch Engine hoạt động theo hai luồng chính: **luồng nạp dữ liệu** (Data Ingestion Flow) và **luồng tìm kiếm** (Search Flow). Hai luồng này chia sẻ chung pipeline tiền xử lý NLP và mô hình TF-IDF, đảm bảo tính nhất quán (consistency) giữa biểu diễn tài liệu và biểu diễn truy vấn — một yêu cầu then chốt trong mọi hệ thống IR [2][8].

**Luồng nạp dữ liệu** bao gồm sáu bước tuần tự:

```
Nguồn dữ liệu (Excel)
  → Tải & Hợp nhất dữ liệu (Pandas)
    → Tiền xử lý NLP (Underthesea: tách từ, loại bỏ từ dừng)
      → Vector hóa TF-IDF (Scikit-learn: fit + transform)
        → Lưu mô hình TF-IDF (joblib → tfidf_vectorizer.pkl)
          → Nạp chỉ mục vào Qdrant (upsert vectors + payload)
```

**Luồng tìm kiếm** bao gồm bốn bước tuần tự:

```
Truy vấn người dùng (query string)
  → Tiền xử lý NLP (cùng pipeline với nạp dữ liệu)
    → Vector hóa TF-IDF (transform bằng mô hình đã lưu — không fit lại)
      → Tìm kiếm tương đồng cosine trên Qdrant → Top K kết quả
```

Điểm mấu chốt trong thiết kế là việc sử dụng **cùng một pipeline tiền xử lý** cho cả hai luồng. Trong luồng nạp dữ liệu, mô hình TF-IDF được huấn luyện (fit) trên toàn bộ kho ngữ liệu và lưu lại dưới dạng tệp pickle. Trong luồng tìm kiếm, mô hình đã lưu được tải lên và chỉ thực hiện biến đổi (transform) truy vấn đầu vào — không huấn luyện lại. Cách tiếp cận này đảm bảo truy vấn và tài liệu được biểu diễn trong cùng một không gian vector, từ đó phép đo tương đồng cosine mới có ý nghĩa toán học [3][14].

---

## 3.2. Thu thập và Tiền xử lý dữ liệu

### 3.2.1. Nguồn dữ liệu và cách thu thập

#### Nguồn dữ liệu

Hệ thống VnSearch Engine sử dụng dữ liệu bài báo tiếng Việt được thu thập từ trang tin tức VnExpress — một trong những trang báo điện tử có lượng truy cập lớn nhất Việt Nam. Dữ liệu bao gồm ba loại thực thể chính: bài viết (articles), danh mục (categories) và bình luận (comments), được lưu trữ dưới dạng ba tệp Excel riêng biệt. Tổng cộng, hệ thống đã thu thập và đánh chỉ mục hơn 2.200 bài viết thuộc 7 danh mục: Khoa học, Ý kiến, Giáo dục, Sức khỏe, Thời sự, Giải trí và Đời sống.

Việc lựa chọn VnExpress làm nguồn dữ liệu xuất phát từ ba lý do. **Thứ nhất**, VnExpress cung cấp nội dung tin tức chất lượng cao, đa dạng chủ đề, với ngôn ngữ tiếng Việt chuẩn — phù hợp cho việc đánh giá hệ thống IR tiếng Việt. **Thứ hai**, cấu trúc trang web và API nội bộ của VnExpress cho phép thu thập dữ liệu một cách có hệ thống thông qua các endpoint có sẵn (Gateway API, Microservice URL). **Thứ ba**, mỗi bài viết đều có tiêu đề, tóm tắt, danh mục và bình luận — cung cấp đủ metadata để xây dựng payload phong phú cho chỉ mục vector.

#### Quy trình thu thập dữ liệu

Quy trình thu thập dữ liệu được tự động hóa thông qua hai thành phần phối hợp: dịch vụ VnExpress Crawler và nền tảng tự động hóa n8n.

Dịch vụ VnExpress Crawler là một ứng dụng FastAPI cung cấp ba nhóm API: thu thập danh mục (`GET /api/v1/categories/`), thu thập bài viết theo danh mục (`GET /api/v1/articles/category/{id}`), và thu thập bình luận (`GET /api/v1/articles/{id}/comments`). Crawler hỗ trợ nhiều chiến lược thu thập: qua Gateway API của VnExpress (lấy bài viết nhanh theo danh mục), qua web scraping (phân tích cú pháp HTML cho các trang phân trang), và theo khoảng ngày (date range) cho phép thu thập dữ liệu lịch sử. Hệ thống tích hợp cơ chế bộ nhớ đệm trong bộ nhớ (in-memory caching) với thời gian sống (TTL) là 3.600 giây cho danh mục và 300 giây cho bài viết, nhằm giảm tải lên máy chủ nguồn.

Nền tảng n8n đóng vai trò điều phối (orchestrator), lập lịch và thực thi các luồng công việc (workflow) thu thập dữ liệu theo cơ chế định thời (cron). Hệ thống triển khai bốn workflow chính: (1) đồng bộ danh mục hàng ngày lúc 02:00 UTC, (2) đồng bộ bài viết hàng ngày lúc 03:00 UTC — duyệt qua tất cả danh mục với cơ chế phân lô (batching) 50–100 danh mục mỗi đợt và độ trễ 100–200ms giữa các yêu cầu, (3) bổ sung dữ liệu hàng tuần (backfill) cho 7 ngày gần nhất, và (4) đồng bộ bình luận hàng tuần cho 500 bài viết có nhiều tương tác nhất. Kết quả được xuất ra các tệp Excel và tải lên Google Drive, đồng thời áp dụng cơ chế loại bỏ trùng lặp (deduplication) theo `article_id` để đảm bảo tính toàn vẹn dữ liệu.

#### Cấu trúc dữ liệu thu thập

Dữ liệu thu thập được tổ chức thành ba tệp Excel với cấu trúc bảng sau:

**Tệp `articles.xlsx`** chứa thông tin bài viết: `article_id` (khóa chính), `category_id` (khóa ngoại liên kết danh mục), `title` (tiêu đề), `summary` (tóm tắt nội dung), `url` (đường dẫn gốc), `thumbnail_url` (ảnh đại diện), `published_at` (thời gian đăng), `source_endpoint` (nguồn thu thập) và `crawled_at` (thời điểm thu thập).

**Tệp `categories.xlsx`** chứa thông tin danh mục: `category_id`, `category_url`, `category_name`, `parent_id` (NULL nếu là danh mục gốc), `level` (root hoặc child), `crawled_at` và `status`.

**Tệp `comments.xlsx`** chứa thông tin bình luận: `article_id` (khóa ngoại), `comment_id` (khóa chính), `author`, `content`, `created_at`, `likes` và `crawled_at`.

### 3.2.2. Cài đặt chuẩn hóa, tách từ và lọc stopwords

#### Tổng quan pipeline tiền xử lý

Sau khi dữ liệu được thu thập và lưu trữ dưới dạng Excel, bước tiếp theo là tiền xử lý văn bản (text preprocessing) — chuyển đổi văn bản thô thành dạng chuẩn hóa phù hợp cho mô hình vector hóa. Pipeline tiền xử lý của hệ thống bao gồm ba bước tuần tự: tách từ tiếng Việt, chuẩn hóa chữ thường và loại bỏ từ dừng. Toàn bộ pipeline được triển khai trong lớp `NLPProcessor` (tệp `app/services/nlp_processor.py`), đảm bảo quy trình xử lý nhất quán giữa giai đoạn nạp dữ liệu và giai đoạn tìm kiếm.

#### Bước 1: Tách từ tiếng Việt (Word Segmentation)

Bước tách từ sử dụng thư viện Underthesea [12] — bộ công cụ NLP cho tiếng Việt dựa trên mô hình Conditional Random Fields (CRF) kết hợp từ điển. Hàm `word_tokenize()` nhận đầu vào là chuỗi văn bản thô và trả về chuỗi đã tách từ, trong đó các từ ghép đa âm tiết được nối bằng dấu gạch dưới. Cụ thể, câu "học sinh học sinh học" sẽ được tách thành "học_sinh học sinh_học", giúp bảo toàn ngữ nghĩa của các từ ghép tiếng Việt.

Trong mã nguồn, bước tách từ được thực hiện như sau:

```python
from underthesea import word_tokenize

tokens = word_tokenize(text, format="text")
```

Tham số `format="text"` chỉ định kết quả trả về dưới dạng chuỗi ký tự (thay vì danh sách), trong đó các từ được phân tách bằng khoảng trắng và các từ ghép được biểu diễn bằng dấu gạch dưới (ví dụ: `"trí_tuệ_nhân_tạo"`). Cách biểu diễn này tương thích trực tiếp với bước vector hóa TF-IDF ở giai đoạn sau, vì mỗi token đa âm tiết được coi là một đặc trưng (feature) duy nhất trong từ điển.

#### Bước 2: Chuẩn hóa chữ thường (Lowercase Normalization)

Sau khi tách từ, toàn bộ văn bản được chuyển về dạng chữ thường (lowercase) nhằm loại bỏ sự phân biệt giữa các biến thể viết hoa và viết thường của cùng một từ. Bước này đảm bảo rằng "Công Nghệ" và "công_nghệ" được coi là cùng một thuật ngữ trong không gian vector. Trong mã nguồn:

```python
words = tokens.lower().split()
```

Phương thức `lower()` chuyển toàn bộ chuỗi về chữ thường, sau đó `split()` tách chuỗi thành danh sách các token riêng lẻ, chuẩn bị cho bước lọc từ dừng tiếp theo.

#### Bước 3: Loại bỏ từ dừng (Stopword Removal)

Từ dừng (stopwords) là các từ xuất hiện với tần suất cao nhưng mang ít giá trị ngữ nghĩa phân biệt — ví dụ: "của", "là", "và", "một", "có", "được", "cho", "không" trong tiếng Việt [13]. Việc loại bỏ từ dừng giúp giảm nhiễu (noise) trong biểu diễn vector, tập trung trọng số vào các thuật ngữ mang ý nghĩa nội dung thực sự, đồng thời giảm kích thước từ điển và tăng tốc quá trình tính toán.

Hệ thống sử dụng một tệp từ dừng tiếng Việt (tệp `assets/txt/vietnamese-stopwords.txt`), được tải và lưu vào bộ nhớ đệm (cache) thông qua module `stopwords_loader.py`. Cơ chế `@lru_cache(maxsize=1)` đảm bảo tệp chỉ được đọc một lần duy nhất từ đĩa, các lần gọi tiếp theo trả về kết quả từ bộ nhớ đệm:

```python
@lru_cache(maxsize=1)
def load_stopwords(stopwords_path: str) -> Set[str]:
    with open(path, "r", encoding="utf-8") as f:
        stopwords = {line.strip() for line in f if line.strip()}
    return stopwords
```

Danh sách từ dừng được lưu trữ dưới dạng tập hợp (set) trong Python, cho phép kiểm tra sự tồn tại của một phần tử với độ phức tạp trung bình O(1). Bước lọc từ dừng trong pipeline tiền xử lý được thực hiện bằng list comprehension:

```python
filtered_words = [word for word in words if word not in self.stopwords]
```

#### Kết quả tiền xử lý

Toàn bộ pipeline trả về chuỗi các token đã qua xử lý, nối bằng khoảng trắng. Ví dụ minh họa quá trình tiền xử lý:

| **Giai đoạn**        | **Kết quả**                                              |
| --------------------- | -------------------------------------------------------- |
| Văn bản gốc           | "Công nghệ trí tuệ nhân tạo đang phát triển mạnh mẽ"    |
| Sau tách từ           | "Công_nghệ trí_tuệ_nhân_tạo đang phát_triển mạnh_mẽ"   |
| Sau chuẩn hóa         | "công_nghệ trí_tuệ_nhân_tạo đang phát_triển mạnh_mẽ"   |
| Sau lọc từ dừng       | "công_nghệ trí_tuệ_nhân_tạo phát_triển mạnh_mẽ"        |

_Bảng 3.2. Ví dụ minh họa pipeline tiền xử lý NLP_

Kết quả cho thấy từ dừng "đang" đã bị loại bỏ, các từ ghép đa âm tiết như "trí_tuệ_nhân_tạo" và "phát_triển" được giữ nguyên dưới dạng token đơn — bảo toàn ngữ nghĩa cho bước vector hóa tiếp theo.

---

## 3.3. Xây dựng mô hình biểu diễn

### 3.3.1. Áp dụng thuật toán TF-IDF trong hệ thống

Mô hình Tần suất thuật ngữ — Tần suất nghịch đảo tài liệu (Term Frequency — Inverse Document Frequency, TF-IDF) là sơ đồ trọng số được sử dụng rộng rãi nhất trong các hệ thống IR truyền thống [14]. Cơ sở lý thuyết của TF-IDF đã được trình bày chi tiết ở Chương 2. Mục này tập trung vào cách áp dụng cụ thể thuật toán TF-IDF trong mã nguồn của hệ thống VnSearch Engine để chuyển đổi tập dữ liệu bài viết thành các vector số học.

Toàn bộ logic vector hóa TF-IDF được triển khai trong lớp `TFIDFService` (tệp `app/services/tfidf_service.py`), sử dụng lớp `TfidfVectorizer` của thư viện Scikit-learn [15]. Quá trình vector hóa được chia thành hai giai đoạn: **huấn luyện** (training/fitting) trên kho ngữ liệu và **biến đổi** (transforming) văn bản thành vector.

### 3.3.2. Giai đoạn huấn luyện mô hình (Fitting)

Giai đoạn huấn luyện diễn ra trong quá trình nạp dữ liệu (ingestion), khi toàn bộ kho ngữ liệu bài viết đã qua tiền xử lý NLP. Mô hình TF-IDF được khởi tạo với các tham số sau:

```python
self.vectorizer = TfidfVectorizer(
    max_features=5000,
    min_df=2,
    max_df=0.8,
    lowercase=False,
    tokenizer=_identity_tokenizer,
    token_pattern=None
)
self.vectorizer.fit(texts)
```

Ý nghĩa của từng tham số được giải thích trong Bảng 3.3:

| **Tham số**      | **Giá trị** | **Ý nghĩa**                                                                                                  |
| ----------------- | ----------- | ------------------------------------------------------------------------------------------------------------- |
| `max_features`    | 5000        | Giới hạn từ điển ở 5.000 thuật ngữ có trọng số TF-IDF cao nhất, giảm chiều không gian vector                  |
| `min_df`          | 2           | Loại bỏ thuật ngữ xuất hiện trong ít hơn 2 tài liệu, lọc bỏ các từ quá hiếm (hapax legomena)                 |
| `max_df`          | 0.8         | Loại bỏ thuật ngữ xuất hiện trong hơn 80% tài liệu, lọc bỏ các từ quá phổ biến (tương tự stopwords)          |
| `lowercase`       | False       | Tắt chuyển đổi chữ thường — vì bước này đã được thực hiện trong pipeline NLP trước đó                         |
| `tokenizer`       | identity    | Sử dụng hàm tách đơn giản `text.split()` — vì văn bản đã được tách từ bởi Underthesea ở bước tiền xử lý      |

_Bảng 3.3. Các tham số cấu hình TfidfVectorizer_

Hàm `_identity_tokenizer` là một hàm tách từ đơn giản chỉ thực hiện `text.split()`, phù hợp cho đầu vào đã qua tiền xử lý:

```python
def _identity_tokenizer(text: str) -> List[str]:
    return text.split()
```

Thiết kế này tuân theo nguyên tắc phân tách trách nhiệm (separation of concerns): bước tách từ tiếng Việt phức tạp (sử dụng Underthesea) được thực hiện hoàn toàn trong pipeline NLP, trong khi TfidfVectorizer chỉ chịu trách nhiệm tính toán trọng số TF-IDF — không can thiệp vào quá trình tokenization.

Phương thức `fit()` của TfidfVectorizer thực hiện ba tác vụ: (1) xây dựng từ điển (vocabulary) từ toàn bộ kho ngữ liệu, áp dụng các bộ lọc `min_df`, `max_df` và `max_features`; (2) tính toán giá trị IDF cho mỗi thuật ngữ trong từ điển theo công thức IDF(t) = log(N/df(t)) + 1, trong đó N là tổng số tài liệu và df(t) là số tài liệu chứa thuật ngữ t [5][6]; (3) lưu trữ ánh xạ từ thuật ngữ sang chỉ số (term-to-index mapping) và vector IDF để sử dụng trong giai đoạn biến đổi.

### 3.3.3. Giai đoạn biến đổi (Transforming)

Sau khi mô hình đã được huấn luyện, phương thức `transform()` chuyển đổi danh sách các văn bản đã qua tiền xử lý thành ma trận TF-IDF:

```python
def transform(self, texts: List[str]) -> np.ndarray:
    vectors = self.vectorizer.transform(texts).toarray()
    return vectors
```

Phương thức `transform()` của TfidfVectorizer trả về một ma trận thưa (sparse matrix) ở định dạng CSR (Compressed Sparse Row), được chuyển đổi sang mảng dày đặc (dense array) bằng `.toarray()` để tương thích với định dạng vector của Qdrant. Mỗi hàng trong ma trận kết quả tương ứng với vector TF-IDF của một tài liệu, có số chiều bằng `max_features` (tối đa 5.000 chiều). Giá trị tại mỗi vị trí biểu diễn trọng số TF-IDF của thuật ngữ tương ứng trong tài liệu đó — giá trị càng cao cho thấy thuật ngữ càng đặc trưng cho tài liệu.

### 3.3.4. Lưu trữ và tải mô hình

Mô hình TF-IDF đã huấn luyện được lưu trữ dưới dạng tệp pickle thông qua thư viện `joblib`, cho phép tải lại nhanh chóng khi hệ thống khởi động hoặc khi xử lý truy vấn tìm kiếm:

```python
# Lưu mô hình
joblib.dump(self.vectorizer, model_path)

# Tải mô hình
self.vectorizer = joblib.load(model_path)
self.is_fitted = True
```

Tệp mô hình được lưu tại đường dẫn `models/tfidf_vectorizer.pkl` (cấu hình qua biến môi trường `TFIDF_MODEL_PATH`). Khi hệ thống khởi động, mô hình được tải tự động vào bộ nhớ — quá trình tìm kiếm chỉ cần gọi `transform()` mà không cần huấn luyện lại, đảm bảo thời gian phản hồi nhanh cho người dùng cuối.

---

## 3.4. Lưu trữ và Quản lý chỉ mục

### 3.4.1. Lựa chọn cơ sở dữ liệu vector Qdrant

Hệ thống VnSearch Engine sử dụng Qdrant [16] làm cơ sở dữ liệu vector (Vector Database) cho việc lưu trữ và tìm kiếm chỉ mục. Qdrant là một cơ sở dữ liệu vector mã nguồn mở, được thiết kế chuyên biệt cho bài toán tìm kiếm tương đồng (similarity search) trên dữ liệu vector chiều cao. So với việc sử dụng cơ sở dữ liệu quan hệ truyền thống (như PostgreSQL) hoặc lưu trữ vector trực tiếp trên tệp tin, Qdrant cung cấp ba ưu điểm chính.

**Thứ nhất, hiệu suất tìm kiếm cao**. Qdrant sử dụng thuật toán HNSW (Hierarchical Navigable Small World) — một thuật toán tìm kiếm láng giềng gần đúng (Approximate Nearest Neighbor — ANN) — cho phép tìm kiếm vector tương đồng với độ phức tạp gần O(log n), nhanh hơn đáng kể so với tìm kiếm tuyến tính O(n) trên toàn bộ tập dữ liệu [16]. Trong thực nghiệm, thời gian tìm kiếm trên Qdrant chỉ mất 10–50ms cho tập dữ liệu hơn 2.200 vector.

**Thứ hai, hỗ trợ payload và lọc kết hợp**. Mỗi vector trong Qdrant có thể gắn kèm payload (metadata) ở dạng JSON, cho phép lọc kết quả theo điều kiện (ví dụ: lọc theo danh mục bài viết) mà không ảnh hưởng đến hiệu suất tìm kiếm vector. Đây là tính năng quan trọng cho phép hệ thống hỗ trợ bộ lọc danh mục (category filter) trong giao diện tìm kiếm.

**Thứ ba, triển khai đơn giản qua Docker**. Qdrant cung cấp Docker image chính thức, cho phép tích hợp liền mạch vào kiến trúc Docker Compose của hệ thống. Dữ liệu được duy trì bền vững (persistent) thông qua volume mount, đảm bảo không mất dữ liệu khi khởi động lại container.

### 3.4.2. Cấu trúc chỉ mục trong Qdrant

Dữ liệu chỉ mục được tổ chức trong một collection (bộ sưu tập) có tên `articles` trên Qdrant. Mỗi bài viết được biểu diễn bằng một điểm dữ liệu (point) bao gồm ba thành phần:

**Thứ nhất, Point ID** — số nguyên tuần tự bắt đầu từ 0, tương ứng với chỉ số hàng trong DataFrame. Hệ thống sử dụng ID tuần tự thay vì `article_id` gốc để đảm bảo tính nhất quán và tránh xung đột khi `article_id` có giá trị âm hoặc không liên tục.

**Thứ hai, Vector** — mảng số thực biểu diễn TF-IDF của bài viết, có số chiều tối đa 5.000 (phụ thuộc vào tham số `max_features`). Vector này là kết quả của quá trình tiền xử lý NLP và biến đổi TF-IDF đã mô tả ở các mục trước.

**Thứ ba, Payload** — đối tượng JSON chứa metadata của bài viết, bao gồm: `article_id` (ID gốc), `title` (tiêu đề), `summary` (tóm tắt), `url` (đường dẫn), `category_name` (tên danh mục), `comment_count` (số bình luận) và `full_text` (văn bản đầy đủ). Payload được trả về cùng với kết quả tìm kiếm, cho phép hiển thị thông tin bài viết mà không cần truy vấn thêm từ nguồn dữ liệu gốc.

### 3.4.3. Quy trình tạo và nạp chỉ mục

Quy trình tạo và nạp chỉ mục được thực hiện bởi lớp `IngestionService` (tệp `app/services/ingestion_service.py`), bao gồm các bước:

**Bước 1: Tạo collection**. Hệ thống kiểm tra sự tồn tại của collection `articles`. Nếu đã tồn tại, collection cũ được xóa và tạo lại mới — đảm bảo dữ liệu chỉ mục luôn đồng bộ với kho ngữ liệu hiện tại. Collection được cấu hình với độ đo khoảng cách cosine (Cosine Distance):

```python
self.client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=vector_dimension,
        distance=Distance.COSINE
    )
)
```

**Bước 2: Chuẩn bị payload**. Với mỗi bài viết trong DataFrame, hệ thống trích xuất các trường metadata và đóng gói thành đối tượng payload:

```python
payload = {
    "article_id": int(row['article_id']),
    "title": str(row['title']),
    "summary": str(row['summary']),
    "url": str(row['url']),
    "category_name": str(row['category_name']),
    "comment_count": int(row['comment_count']),
    "full_text": str(row['full_text'])
}
```

**Bước 3: Nạp vector theo lô (Batch Upsert)**. Các vector và payload được nạp vào Qdrant theo lô (batch) với kích thước 100 điểm mỗi lô, sử dụng phương thức `upsert()`:

```python
batch_size = 100
for i in range(0, len(points), batch_size):
    batch = points[i:i + batch_size]
    self.client.upsert(
        collection_name=collection_name,
        points=batch
    )
```

Cơ chế nạp theo lô giúp kiểm soát mức tiêu thụ bộ nhớ và tránh gây quá tải cho Qdrant khi số lượng vector lớn. Phương thức `upsert()` (update + insert) đảm bảo rằng nếu một point ID đã tồn tại, dữ liệu sẽ được cập nhật thay vì tạo trùng lặp.

---

## 3.5. Xử lý truy vấn tìm kiếm

### 3.5.1. Luồng xử lý truy vấn

Khi người dùng nhập câu truy vấn tìm kiếm thông qua giao diện web, hệ thống thực hiện bốn bước xử lý tuần tự tại endpoint `POST /api/v1/search` (tệp `app/api/v1/search.py`). Toàn bộ quá trình được đo thời gian thực thi để báo cáo cho người dùng.

**Bước 1: Tiền xử lý truy vấn (Query Preprocessing)**. Truy vấn của người dùng được đưa qua cùng pipeline NLP đã sử dụng trong giai đoạn nạp dữ liệu — bao gồm tách từ bằng Underthesea, chuẩn hóa chữ thường và loại bỏ từ dừng:

```python
processed_query = nlp_processor.preprocess(request.query)
```

Nếu sau quá trình tiền xử lý, truy vấn trở thành chuỗi rỗng (ví dụ: truy vấn chỉ chứa toàn từ dừng như "của và là"), hệ thống trả về mã lỗi 400 (Bad Request) kèm thông báo giải thích. Điều này ngăn chặn việc gửi vector toàn số không (zero vector) đến Qdrant — một truy vấn vô nghĩa sẽ trả về kết quả ngẫu nhiên.

**Bước 2: Vector hóa truy vấn (Query Vectorization)**. Truy vấn đã qua tiền xử lý được biến đổi thành vector TF-IDF bằng mô hình đã huấn luyện và lưu trữ sẵn:

```python
query_vector = tfidf_service.transform([processed_query])[0]
```

Lưu ý rằng phương thức `transform()` được sử dụng thay vì `fit_transform()` — mô hình không được huấn luyện lại trên truy vấn mà chỉ áp dụng bộ trọng số IDF đã học từ kho ngữ liệu. Đây là điểm thiết kế quan trọng: truy vấn được biểu diễn trong cùng không gian vector với tập tài liệu, đảm bảo phép đo tương đồng cosine có ý nghĩa [3].

**Bước 3: Tìm kiếm tương đồng trên Qdrant (Similarity Search)**. Vector truy vấn được gửi đến Qdrant để tìm kiếm các vector tài liệu có độ tương đồng cosine cao nhất:

```python
search_results = qdrant.search(
    collection_name=settings.qdrant_collection_name,
    query_vector=query_vector,
    limit=request.limit,
    category_filter=request.category_filter
)
```

Tham số `limit` xác định số lượng kết quả tối đa trả về (mặc định 10, tối đa 100). Tham số `category_filter` cho phép lọc kết quả theo danh mục bài viết — Qdrant thực hiện lọc này trực tiếp trên payload trước khi tính toán tương đồng, đảm bảo hiệu suất không bị ảnh hưởng.

### 3.5.2. Cơ chế tính toán thứ hạng kết quả

Qdrant sử dụng Độ tương đồng cosine (Cosine Similarity) làm độ đo khoảng cách giữa vector truy vấn và các vector tài liệu. Công thức tính được biểu diễn như sau:

```
cosine_similarity(q, d) = (q · d) / (‖q‖ × ‖d‖)
```

Trong đó `q` là vector truy vấn, `d` là vector tài liệu, `q · d` là tích vô hướng (dot product) và `‖·‖` là chuẩn Euclid (L2 norm). Giá trị kết quả nằm trong khoảng [0, 1] (do các vector TF-IDF không âm), trong đó giá trị càng gần 1 biểu thị mức độ tương đồng ngữ nghĩa càng cao [3][5].

Qdrant trả về kết quả đã được sắp xếp theo thứ tự giảm dần của điểm tương đồng (score). Mỗi kết quả bao gồm: Point ID, điểm tương đồng (score) và toàn bộ payload metadata. Hệ thống không áp dụng ngưỡng cắt (threshold) cứng cho điểm tương đồng — tất cả Top K kết quả đều được trả về, và điểm số được hiển thị trên giao diện để người dùng tự đánh giá mức độ liên quan.

### 3.5.3. Xây dựng và trả về kết quả

Kết quả từ Qdrant được ánh xạ thành danh sách các đối tượng `ArticleResult`, mỗi đối tượng chứa: `id` (Point ID), `score` (điểm tương đồng cosine), `article_id` (ID bài viết gốc), `title`, `summary`, `url`, `category_name` và `comment_count`. Phản hồi cuối cùng (`SearchResponse`) bao gồm: truy vấn gốc, truy vấn sau xử lý NLP, tổng số kết quả, danh sách kết quả và thời gian thực thi (tính bằng mili-giây):

```python
return SearchResponse(
    query=request.query,
    processed_query=processed_query,
    total_results=len(articles),
    results=articles,
    execution_time_ms=round(execution_time_ms, 2)
)
```

Việc trả về cả `query` gốc và `processed_query` cho phép người dùng quan sát sự khác biệt giữa đầu vào ban đầu và kết quả tiền xử lý NLP — giúp hiểu rõ hơn cách hệ thống "hiểu" truy vấn của mình. Thời gian thực thi trung bình cho toàn bộ luồng tìm kiếm đạt khoảng 200ms, bao gồm: tiền xử lý NLP (20–50ms), vector hóa TF-IDF (30–80ms), tìm kiếm trên Qdrant (10–50ms) và xây dựng phản hồi (5–20ms).

---

## Tài liệu tham khảo Chương 3

[2] C. D. Manning, P. Raghavan, and H. Schütze, _Introduction to Information Retrieval_, Cambridge University Press, 2008.

[3] G. Salton, A. Wong, and C. S. Yang, "A Vector Space Model for Automatic Indexing," _Communications of the ACM_, vol. 18, no. 11, pp. 613–620, 1975.

[5] G. Salton and M. J. McGill, _Introduction to Modern Information Retrieval_, McGraw-Hill, 1983.

[6] K. Sparck Jones, "A Statistical Interpretation of Term Specificity and Its Application in Retrieval," _Journal of Documentation_, vol. 28, no. 1, pp. 11–21, 1972.

[8] R. Baeza-Yates and B. Ribeiro-Neto, _Modern Information Retrieval: The Concepts and Technology Behind Search_, 2nd ed., Addison-Wesley, 2011.

[12] V. T. Vu, "Underthesea — Vietnamese NLP Toolkit," _GitHub Repository_, 2017. [Trực tuyến]. Truy cập: https://github.com/undertheseanlp/underthesea

[13] H. T. Nguyen and T. M. H. Nguyen, "Vietnamese Stopword Removal for Text Classification," _Journal of Computer Science and Cybernetics_, vol. 29, no. 2, pp. 145–157, 2013.

[14] G. Salton and C. Buckley, "Term-Weighting Approaches in Automatic Text Retrieval," _Information Processing & Management_, vol. 24, no. 5, pp. 513–523, 1988.

[15] F. Pedregosa _et al._, "Scikit-learn: Machine Learning in Python," _Journal of Machine Learning Research_, vol. 12, pp. 2825–2830, 2011.

[16] Qdrant Team, "Qdrant — Vector Search Engine," _Qdrant Documentation_, 2023. [Trực tuyến]. Truy cập: https://qdrant.tech/documentation/

[20] S. Newman, _Building Microservices: Designing Fine-Grained Systems_, 2nd ed., O'Reilly Media, 2021.

> **Ghi chú**: Tài liệu [2], [3], [5], [6], [8] đã được giới thiệu ở Chương 1 và Chương 2; tài liệu [12], [13], [14], [15], [16] đã được giới thiệu ở Chương 2. Các tài liệu này được trích dẫn lại ở Chương 3 với cùng số thứ tự để đảm bảo tính nhất quán. Tài liệu mới của Chương 3 là [20].
