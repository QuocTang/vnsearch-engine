# CHƯƠNG 1. TỔNG QUAN

## 1.1. Giới thiệu đề tài

### 1.1.1. Bối cảnh nghiên cứu

Trong bối cảnh bùng nổ thông tin số hiện nay, lượng dữ liệu phi cấu trúc — đặc biệt là văn bản — đang tăng trưởng với tốc độ chưa từng có. Theo ước tính của International Data Corporation (IDC), tổng lượng dữ liệu toàn cầu đã đạt hơn 120 Zettabyte vào năm 2023 và được dự báo sẽ tiếp tục tăng gấp đôi sau mỗi hai năm [1]. Trong đó, dữ liệu văn bản chiếm một tỷ trọng đáng kể, bao gồm các bài báo trực tuyến, bài đăng trên mạng xã hội, blog, tài liệu kỹ thuật và nhiều nguồn nội dung số khác. Việc tìm kiếm và truy xuất thông tin chính xác từ khối lượng dữ liệu khổng lồ này trở thành một thách thức cốt lõi trong lĩnh vực Khoa học Máy tính và Xử lý Ngôn ngữ Tự nhiên (Natural Language Processing — NLP).

Truy hồi thông tin (Information Retrieval — IR) là lĩnh vực nghiên cứu về các phương pháp tìm kiếm, trích xuất và xếp hạng các tài liệu có liên quan đến nhu cầu thông tin của người dùng từ một tập hợp tài liệu lớn [2]. Khác với truy vấn cơ sở dữ liệu truyền thống — nơi dữ liệu được tổ chức theo cấu trúc bảng rõ ràng và truy vấn cho kết quả chính xác tuyệt đối — truy hồi thông tin phải đối mặt với bản chất mơ hồ, đa nghĩa và thiếu cấu trúc của ngôn ngữ tự nhiên. Một truy vấn tìm kiếm như _"ảnh hưởng biến đổi khí hậu đến nông nghiệp"_ có thể liên quan đến hàng nghìn tài liệu với mức độ phù hợp khác nhau, và hệ thống cần đủ "thông minh" để xếp hạng các tài liệu theo mức độ liên quan (relevance) thay vì chỉ đơn thuần trả về những tài liệu chứa đúng các từ khóa đó.

### 1.1.2. Bài toán tìm kiếm và truy hồi thông tin

Bài toán truy hồi thông tin có thể được phát biểu một cách hình thức như sau: cho một tập hợp tài liệu _D = {d₁, d₂, ..., dₙ}_ và một truy vấn _q_ biểu diễn nhu cầu thông tin của người dùng, mục tiêu là tìm ra tập con _R ⊆ D_ sao cho các tài liệu trong _R_ có mức độ liên quan cao nhất đối với _q_, đồng thời sắp xếp chúng theo thứ tự giảm dần của mức độ liên quan.

Trong lịch sử phát triển của lĩnh vực IR, nhiều mô hình biểu diễn và truy hồi đã được đề xuất, có thể phân thành ba nhóm chính:

- **Mô hình Boolean (Boolean Model)**: Là mô hình cổ điển nhất, dựa trên lý thuyết tập hợp và đại số Boole [2][3]. Mỗi tài liệu được biểu diễn bằng tập hợp các thuật ngữ (terms), và truy vấn là một biểu thức logic kết hợp các thuật ngữ bằng các toán tử AND, OR, NOT. Mô hình Boolean có ưu điểm là đơn giản, dễ triển khai, tuy nhiên nhược điểm lớn nhất là không có khả năng xếp hạng kết quả — một tài liệu hoặc phù hợp hoặc không phù hợp, không có mức độ trung gian.

- **Mô hình xác suất (Probabilistic Model)**: Tiếp cận bài toán IR từ góc độ xác suất thống kê, ước lượng xác suất một tài liệu phù hợp với truy vấn dựa trên các đặc trưng thống kê của thuật ngữ [4]. Các mô hình tiêu biểu bao gồm BM25 (Best Matching 25) hiện vẫn được sử dụng rộng rãi trong các hệ thống tìm kiếm hiện đại như Elasticsearch và Apache Lucene.

- **Mô hình không gian vector (Vector Space Model — VSM)**: Được đề xuất bởi Salton và cộng sự (1975) [3], đây là mô hình biểu diễn tài liệu và truy vấn dưới dạng các vector trong không gian nhiều chiều. Mỗi chiều tương ứng với một thuật ngữ trong từ điển (vocabulary), và giá trị tại mỗi chiều phản ánh mức độ quan trọng (trọng số) của thuật ngữ đó trong tài liệu. Mức độ liên quan giữa tài liệu và truy vấn được đo bằng độ tương đồng giữa hai vector, thông thường sử dụng **độ tương đồng cosine (Cosine Similarity)**. Mô hình VSM khắc phục được nhược điểm của mô hình Boolean bằng việc cho phép xếp hạng kết quả theo mức độ liên quan liên tục.

Trong mô hình VSM, lựa chọn phương pháp gán trọng số cho thuật ngữ đóng vai trò then chốt. **TF-IDF (Term Frequency — Inverse Document Frequency)** là sơ đồ trọng số được sử dụng phổ biến nhất [6]. TF-IDF kết hợp hai yếu tố: tần suất xuất hiện của thuật ngữ trong tài liệu (TF) và mức độ phân biệt của thuật ngữ trong toàn bộ tập tài liệu (IDF). Thuật ngữ xuất hiện nhiều trong một tài liệu nhưng hiếm trong toàn bộ tập hợp sẽ có trọng số cao, phản ánh đúng tính chất phân biệt (discriminative) của thuật ngữ đó đối với tài liệu.

### 1.1.3. Thách thức đối với tiếng Việt

Mặc dù các mô hình IR đã đạt được nhiều thành tựu đáng kể trên các ngôn ngữ phổ biến như tiếng Anh, việc áp dụng chúng cho tiếng Việt đặt ra một số thách thức đặc thù:

**Thứ nhất**, tiếng Việt là ngôn ngữ đơn lập (isolating language), trong đó ranh giới từ không được đánh dấu rõ ràng bằng khoảng trắng như tiếng Anh. Một "từ" tiếng Việt có thể bao gồm một hoặc nhiều âm tiết, ví dụ: _"học sinh"_, _"máy tính"_, _"trí tuệ nhân tạo"_. Do đó, bài toán **tách từ (word segmentation)** trở thành bước tiền xử lý bắt buộc và có ảnh hưởng trực tiếp đến chất lượng truy hồi [7]. Nếu hệ thống tách sai — chẳng hạn tách _"học sinh"_ thành hai token _"học"_ và _"sinh"_ riêng biệt — thì ngữ nghĩa sẽ bị biến đổi hoàn toàn, dẫn đến kết quả tìm kiếm sai lệch.

**Thứ hai**, tiếng Việt có hệ thống dấu thanh phức tạp (sáu thanh điệu), tạo ra sự đa dạng về mặt hình thái học. Cùng một chuỗi ký tự khi bỏ dấu có thể tương ứng với nhiều từ có nghĩa khác nhau, gây khó khăn cho quá trình chuẩn hóa văn bản. Ngoài ra, người dùng Việt Nam có thói quen viết không dấu hoặc viết tắt trên các nền tảng trực tuyến, đòi hỏi hệ thống phải có khả năng xử lý linh hoạt.

**Thứ ba**, tài nguyên xử lý ngôn ngữ tự nhiên cho tiếng Việt vẫn còn hạn chế so với tiếng Anh. Các thư viện NLP phổ biến như NLTK, spaCy chủ yếu tập trung vào tiếng Anh và một số ngôn ngữ châu Âu. Đối với tiếng Việt, các công cụ như **Underthesea**, VnCoreNLP, PyVi đã được phát triển nhưng vẫn cần được đánh giá và tối ưu hóa thêm trong bối cảnh các ứng dụng thực tế.

**Thứ tư**, danh sách **từ dừng (stopwords)** tiếng Việt — tức các từ xuất hiện rất phổ biến nhưng không mang nhiều giá trị ngữ nghĩa như _"và"_, _"của"_, _"là"_, _"những"_, _"thì"_ — cần được xây dựng và chuẩn hóa riêng. Việc loại bỏ từ dừng hiệu quả giúp giảm nhiễu cho mô hình vector hóa, cải thiện cả hiệu suất tính toán lẫn chất lượng truy hồi.

### 1.1.4. Xu hướng hiện đại và vị trí của đề tài

Trong những năm gần đây, sự phát triển mạnh mẽ của các mô hình ngôn ngữ lớn (Large Language Models — LLM) và các kỹ thuật nhúng ngữ nghĩa (semantic embedding) như BERT, Sentence-BERT đã mở ra kỷ nguyên mới cho bài toán tìm kiếm ngữ nghĩa (semantic search). Tuy nhiên, mô hình Vector Space Model kết hợp TF-IDF vẫn giữ vai trò quan trọng trong thực tế vì nhiều lý do:

- **Tính khả diễn giải (Interpretability)**: Trọng số TF-IDF có ý nghĩa thống kê rõ ràng, cho phép giải thích tại sao một tài liệu được xếp hạng cao cho một truy vấn nhất định.
- **Hiệu quả tính toán**: Không yêu cầu tài nguyên GPU đắt đỏ cho quá trình inference như các mô hình deep learning.
- **Phù hợp với quy mô dữ liệu vừa và lớn**: Kết hợp với các cơ sở dữ liệu vector chuyên dụng (như Qdrant, Milvus, Faiss), có thể phục vụ hàng triệu tài liệu với thời gian phản hồi ở mức mili-giây.
- **Nền tảng lý thuyết vững chắc**: Là cơ sở để hiểu và so sánh với các phương pháp hiện đại hơn.

Đề tài này được thực hiện trong bối cảnh đó — nhằm xây dựng một hệ thống truy hồi thông tin hoàn chỉnh cho tiếng Việt, từ khâu thu thập dữ liệu, tiền xử lý ngôn ngữ, vector hóa, đến tìm kiếm và trình bày kết quả, sử dụng nền tảng lý thuyết của Vector Space Model kết hợp TF-IDF làm cốt lõi.

---

## 1.2. Mục tiêu đề tài

### 1.2.1. Mục tiêu tổng quát

Xây dựng một **Hệ thống Truy hồi Thông tin tiếng Việt (Vietnamese Information Retrieval System — IRS)** hoàn chỉnh, dựa trên tiếp cận **Mô hình Không gian Vector (Vector Space Model)** kết hợp sơ đồ trọng số **TF-IDF (Term Frequency — Inverse Document Frequency)**, có khả năng tìm kiếm ngữ nghĩa trên tập dữ liệu bài báo tiếng Việt quy mô lớn với thời gian phản hồi thấp và độ chính xác cao.

### 1.2.2. Mục tiêu cụ thể

Để hiện thực hóa mục tiêu tổng quát, đề tài đặt ra các mục tiêu cụ thể sau:

**Mục tiêu 1 — Xây dựng Pipeline thu thập và tiền xử lý dữ liệu tự động:**

- Thiết kế và triển khai hệ thống thu thập dữ liệu (Crawler) tự động từ nguồn tin tức trực tuyến VnExpress — một trong những trang báo điện tử lớn nhất Việt Nam — bao gồm ba loại dữ liệu: danh mục (categories), bài viết (articles) và bình luận (comments).
- Xây dựng quy trình tự động hóa (workflow automation) sử dụng n8n để lên lịch thu thập dữ liệu định kỳ (daily sync, weekly backfill), đảm bảo tập dữ liệu luôn được cập nhật.
- Triển khai pipeline tiền xử lý ngôn ngữ tự nhiên cho tiếng Việt: tách từ (word segmentation) bằng thư viện Underthesea, chuẩn hóa văn bản (lowercasing), và loại bỏ từ dừng (stopword removal) sử dụng danh sách từ dừng tiếng Việt chuyên dụng.

**Mục tiêu 2 — Triển khai mô hình Vector Space Model với TF-IDF:**

- Xây dựng mô hình vector hóa văn bản sử dụng TfidfVectorizer từ thư viện Scikit-learn, huấn luyện trên toàn bộ tập dữ liệu bài báo đã tiền xử lý.
- Lưu trữ các vector kết quả trong cơ sở dữ liệu vector chuyên dụng Qdrant, cùng với metadata (tiêu đề, tóm tắt, URL, danh mục, số bình luận) dưới dạng payload.
- Triển khai cơ chế tìm kiếm tương đồng sử dụng **độ tương đồng cosine (Cosine Similarity)** với khả năng lọc kết quả theo danh mục và giới hạn số lượng trả về.

**Mục tiêu 3 — Phát triển hệ thống API và giao diện người dùng:**

- Thiết kế và xây dựng RESTful API sử dụng framework FastAPI (Python), cung cấp các endpoint cho kiểm tra sức khỏe hệ thống (health check), tìm kiếm (search) và kích hoạt nạp dữ liệu (ingestion).
- Phát triển giao diện web hiện đại, đáp ứng (responsive) sử dụng Next.js 16, React 19, TailwindCSS 4 và Shadcn UI, tích hợp các tính năng nâng cao: lịch sử tìm kiếm, bộ lọc danh mục, chế độ sáng/tối (dark mode), hiệu ứng 3D (Three.js), và tối ưu SEO.

**Mục tiêu 4 — Đảm bảo hiệu suất và khả năng triển khai:**

- Đạt thời gian phản hồi API tìm kiếm dưới 500ms (trong đó thời gian tìm kiếm vector dưới 50ms).
- Đóng gói toàn bộ hệ thống bằng Docker Compose theo kiến trúc Microservices, cho phép triển khai nhanh chóng trên bất kỳ máy chủ nào.
- Đảm bảo tính bền vững dữ liệu thông qua volume mounting và cơ chế health check tự động.

---

## 1.3. Phạm vi và giới hạn đề tài

### 1.3.1. Phạm vi nghiên cứu

Đề tài tập trung vào các khía cạnh sau:

**Về mặt ngôn ngữ:**

- Đối tượng xử lý là **văn bản tiếng Việt** — cụ thể là các bài báo tin tức trực tuyến viết bằng tiếng Việt có dấu, sử dụng bảng mã Unicode (UTF-8).
- Các kỹ thuật xử lý ngôn ngữ tự nhiên được thiết kế riêng cho tiếng Việt, bao gồm tách từ (word segmentation) bằng Underthesea và bộ từ dừng (stopwords) tiếng Việt chuyên dụng.

**Về mặt dữ liệu:**

- Nguồn dữ liệu được thu thập từ **VnExpress** (vnexpress.net) — trang báo điện tử có lượng truy cập hàng đầu tại Việt Nam, với nội dung phong phú trải rộng trên nhiều danh mục: Thời sự, Khoa học, Giáo dục, Sức khỏe, Ý kiến, Giải trí, Đời sống, và nhiều lĩnh vực khác.
- Quy mô dữ liệu đạt mức hàng nghìn bài viết (khoảng 2.000 — 5.000 bài báo), bao gồm đầy đủ thông tin: tiêu đề, tóm tắt, URL, hình ảnh thu nhỏ (thumbnail), danh mục, ngày xuất bản và số lượng bình luận.
- Hệ thống thu thập dữ liệu bao phủ hơn 2.366 danh mục từ VnExpress, hỗ trợ thu thập gia tăng (incremental) theo ngày.

**Về mặt thuật toán và mô hình:**

- Áp dụng **Mô hình Không gian Vector (Vector Space Model)** làm nền tảng biểu diễn tài liệu và truy vấn.
- Sử dụng sơ đồ trọng số **TF-IDF** để gán trọng số cho các thuật ngữ trong vector.
- Sử dụng **độ tương đồng cosine (Cosine Similarity)** làm thước đo mức độ liên quan giữa truy vấn và tài liệu.
- Lưu trữ và tìm kiếm vector thông qua cơ sở dữ liệu vector chuyên dụng **Qdrant**.

**Về mặt kiến trúc hệ thống:**

- Hệ thống được thiết kế theo kiến trúc **Microservices**, bao gồm 6 thành phần: Backend API (FastAPI), Frontend Web (Next.js), Crawler API (FastAPI), Workflow Engine (n8n), Vector Database (Qdrant) và Relational Database (PostgreSQL).
- Toàn bộ hệ thống được đóng gói bằng **Docker Compose** để đảm bảo tính nhất quán môi trường và dễ dàng triển khai.

### 1.3.2. Giới hạn đề tài

Đề tài nhận thức rõ các giới hạn sau đây:

**Về mặt ngôn ngữ và dữ liệu:**

- Hệ thống chỉ xử lý **văn bản tiếng Việt có dấu**. Các truy vấn hoặc tài liệu viết không dấu, viết tắt, hoặc sử dụng ngôn ngữ lóng (slang) chưa được hỗ trợ tối ưu.
- Dữ liệu được giới hạn từ một nguồn duy nhất là VnExpress. Việc mở rộng sang các nguồn tin tức khác (Tuổi Trẻ, Thanh Niên, Dân Trí, v.v.) hoặc dữ liệu mạng xã hội (Facebook, Twitter/X) nằm ngoài phạm vi đề tài hiện tại.
- Quy mô dữ liệu ở mức hàng nghìn tài liệu. Việc đánh giá hiệu suất trên tập dữ liệu hàng triệu tài liệu chưa được thực hiện trong phiên bản này.

**Về mặt thuật toán:**

- Đề tài sử dụng phương pháp TF-IDF truyền thống — thuộc nhóm sparse vector. Các phương pháp nhúng ngữ nghĩa sâu (dense embedding) như BERT, PhoBERT, Sentence-BERT cho tiếng Việt **không nằm trong phạm vi** của đề tài, mặc dù kiến trúc hệ thống cho phép tích hợp trong tương lai.
- Mô hình TF-IDF có hạn chế về khả năng nắm bắt ngữ nghĩa ở mức độ sâu — không xử lý được các trường hợp đồng nghĩa (synonymy) hoặc đa nghĩa (polysemy) một cách tường minh.

**Về mặt đánh giá:**

- Chưa có bộ dữ liệu benchmark chuẩn (ground truth) cho bài toán truy hồi thông tin tiếng Việt trên dữ liệu tin tức, do đó việc đánh giá định lượng bằng các chỉ số chuẩn như Precision@K, Recall@K, MAP (Mean Average Precision) hay NDCG (Normalized Discounted Cumulative Gain) sẽ được thực hiện ở mức cơ bản với đánh giá thủ công.
- Đề tài tập trung vào **tính khả thi kỹ thuật** (technical feasibility) và **hiệu suất thời gian phản hồi** (response time performance) hơn là đánh giá toàn diện chất lượng truy hồi trên bộ test set lớn.

**Về mặt bảo mật và vận hành:**

- Hệ thống được xây dựng cho mục đích nghiên cứu và học tập, chưa tích hợp cơ chế xác thực người dùng (authentication), phân quyền (authorization) hay mã hóa dữ liệu.
- Cấu hình CORS (Cross-Origin Resource Sharing) hiện cho phép tất cả các origin, cần được hạn chế khi triển khai trên môi trường production.

---

## Tài liệu tham khảo Chương 1

[1] D. Reinsel, J. Gantz, and J. Rydning, "The Digitization of the World — From Edge to Core," _IDC White Paper_, 2018.

[2] C. D. Manning, P. Raghavan, and H. Schütze, _Introduction to Information Retrieval_, Cambridge University Press, 2008.

[3] G. Salton, A. Wong, and C. S. Yang, "A Vector Space Model for Automatic Indexing," _Communications of the ACM_, vol. 18, no. 11, pp. 613–620, 1975.

[4] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," _Foundations and Trends in Information Retrieval_, vol. 3, no. 4, pp. 333–389, 2009.

[5] G. Salton and M. J. McGill, _Introduction to Modern Information Retrieval_, McGraw-Hill, 1983.

[6] K. Sparck Jones, "A Statistical Interpretation of Term Specificity and Its Application in Retrieval," _Journal of Documentation_, vol. 28, no. 1, pp. 11–21, 1972.

[7] Nguyen T. P., Nguyen V. H., Le H. P., "A Hybrid Approach to Vietnamese Word Segmentation," _Proceedings of the IEEE RIVF International Conference on Computing and Communication Technologies_, 2008.

> **Ghi chú**: Tài liệu [2] (Manning et al., 2008) trình bày tổng quan về cả ba mô hình: Boolean, Probabilistic và Vector Space Model, được sử dụng làm tài liệu tham chiếu chung cho phần 1.1.2. Tài liệu [3] (Salton et al., 1975) là bài báo gốc đề xuất Vector Space Model. Tài liệu [5] (Salton & McGill, 1983) là chuyên khảo mở rộng về các phương pháp truy hồi thông tin hiện đại.
