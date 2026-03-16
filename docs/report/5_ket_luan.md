# CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

Chương này tổng kết toàn bộ quá trình nghiên cứu và xây dựng hệ thống truy hồi thông tin ngữ nghĩa tiếng Việt — VnSearch Engine. Nội dung bao gồm: đánh giá mức độ hoàn thành các mục tiêu đã đề ra ở Chương 1, phân tích các hạn chế còn tồn tại của hệ thống, và đề xuất các hướng phát triển trong tương lai nhằm nâng cao chất lượng truy hồi và mở rộng phạm vi ứng dụng.

---

## 5.1. Kết quả đạt được

Đối chiếu với bốn nhóm mục tiêu cụ thể đã đề ra ở mục 1.2.2, đề tài đã đạt được các kết quả sau:

### 5.1.1. Mục tiêu 1 — Pipeline thu thập và tiền xử lý dữ liệu tự động

Hệ thống đã xây dựng thành công pipeline thu thập dữ liệu tự động từ VnExpress thông qua dịch vụ VnExpress Crawler kết hợp nền tảng tự động hóa n8n. Cụ thể, Crawler cung cấp ba nhóm API (danh mục, bài viết, bình luận) với nhiều chiến lược thu thập (Gateway API, web scraping, lọc theo ngày), hỗ trợ bộ nhớ đệm trong bộ nhớ (in-memory caching) để giảm tải lên máy chủ nguồn. Nền tảng n8n điều phối bốn workflow định thời: đồng bộ danh mục hàng ngày, đồng bộ bài viết hàng ngày với cơ chế phân lô và loại bỏ trùng lặp, bổ sung dữ liệu hàng tuần (backfill), và đồng bộ bình luận hàng tuần. Kết quả thu thập đạt **hơn 2.200 bài viết** thuộc **7 danh mục** chính, vượt ngưỡng tối thiểu 1.000 tài liệu đặt ra cho đề tài.

Pipeline tiền xử lý Xử lý Ngôn ngữ Tự nhiên (Natural Language Processing — NLP) cho tiếng Việt đã được triển khai hoàn chỉnh với ba bước tuần tự: tách từ bằng Underthesea [12], chuẩn hóa chữ thường và loại bỏ từ dừng sử dụng danh sách từ dừng tiếng Việt chuyên dụng. Điểm nổi bật trong thiết kế là việc đảm bảo **tính nhất quán tuyệt đối** của pipeline giữa giai đoạn nạp dữ liệu và giai đoạn tìm kiếm — cả hai đều sử dụng cùng một lớp `NLPProcessor` — đây là yêu cầu then chốt để phép đo Độ tương đồng cosine (Cosine Similarity) có ý nghĩa toán học trong Mô hình Không gian Vector (Vector Space Model — VSM) [3].

### 5.1.2. Mục tiêu 2 — Triển khai mô hình Vector Space Model với TF-IDF

Mô hình vector hóa Tần suất thuật ngữ — Tần suất nghịch đảo tài liệu (Term Frequency — Inverse Document Frequency, TF-IDF) đã được triển khai thành công sử dụng `TfidfVectorizer` của thư viện Scikit-learn [15], với cấu hình phù hợp cho dữ liệu tiếng Việt: giới hạn từ điển 5.000 đặc trưng, lọc thuật ngữ quá hiếm (`min_df=2`) và quá phổ biến (`max_df=0.8`), kết hợp hàm tách từ đồng nhất (identity tokenizer) cho đầu vào đã qua tiền xử lý. Mô hình đã huấn luyện được lưu trữ dưới dạng tệp pickle và tải tự động khi hệ thống khởi động, đảm bảo quá trình tìm kiếm chỉ cần thực hiện biến đổi (transform) mà không cần huấn luyện lại.

Các vector TF-IDF (khoảng 3.740 chiều trên tập dữ liệu hiện tại) được lưu trữ trong cơ sở dữ liệu vector Qdrant [16] cùng với payload metadata đầy đủ (tiêu đề, tóm tắt, URL, danh mục, số bình luận). Cơ chế tìm kiếm tương đồng cosine trên Qdrant hoạt động chính xác, hỗ trợ lọc kết quả theo danh mục (category filter) thông qua cơ chế lọc payload tại tầng cơ sở dữ liệu — không ảnh hưởng đến hiệu suất tìm kiếm vector.

### 5.1.3. Mục tiêu 3 — Hệ thống API và giao diện người dùng

Hệ thống RESTful API đã được xây dựng trên framework FastAPI với ba endpoint chính: kiểm tra sức khỏe (`GET /`), tìm kiếm ngữ nghĩa (`POST /api/v1/search`) và kích hoạt nạp dữ liệu (`POST /api/v1/ingest`). API được thiết kế theo tiêu chuẩn OpenAPI, tự động sinh tài liệu Swagger cho phép kiểm thử trực tiếp trên trình duyệt. Mỗi phản hồi tìm kiếm cung cấp đầy đủ thông tin: truy vấn gốc, truy vấn sau xử lý NLP, tổng số kết quả, danh sách bài viết kèm điểm tương đồng và thời gian thực thi.

Giao diện web được phát triển theo triết lý Minimalist Search Engine sử dụng Next.js 16, React 19 và TailwindCSS 4. Các tính năng đã hoàn thành bao gồm: thanh tìm kiếm với xác thực đầu vào (Zod) và cơ chế chống gửi liên tục (debounce 300ms), bộ lọc danh mục và giới hạn kết quả, hiển thị kết quả dạng lưới đáp ứng (responsive grid) với Article Card, lịch sử tìm kiếm (Zustand + localStorage), chế độ sáng/tối (Dark/Light Mode), hiệu ứng 3D (React Three Fiber) và tối ưu SEO. Giao diện hoạt động tốt trên cả ba nền tảng: điện thoại di động, máy tính bảng và máy tính để bàn.

### 5.1.4. Mục tiêu 4 — Hiệu suất và khả năng triển khai

Kết quả thực nghiệm tại Chương 4 cho thấy hệ thống đáp ứng tốt các chỉ tiêu hiệu suất đã đề ra. Thời gian phản hồi API tìm kiếm trung bình đạt khoảng **200ms** (dưới ngưỡng mục tiêu 500ms), trong đó thời gian tìm kiếm vector trên Qdrant chỉ mất **10–50ms** (dưới ngưỡng mục tiêu 50ms). Thời gian phản hồi tổng thể nằm dưới ngưỡng nhận thức "tức thì" 1 giây của người dùng [19], đảm bảo trải nghiệm tìm kiếm mượt mà.

Toàn bộ hệ thống gồm năm dịch vụ (IRS API, IRS Web, Qdrant, n8n, PostgreSQL) được đóng gói và triển khai bằng Docker Compose, cho phép khởi động toàn bộ hệ thống bằng một lệnh duy nhất (`./setup/start.sh`). Dữ liệu được duy trì bền vững thông qua volume mount, và cơ chế health check tự động giám sát trạng thái các dịch vụ quan trọng theo chu kỳ 30 giây.

### 5.1.5. Tổng hợp đánh giá

Bảng 5.1 tổng hợp mức độ hoàn thành từng mục tiêu cụ thể:

| **Mục tiêu**                                    | **Kết quả**                                                  | **Đánh giá**  |
| ------------------------------------------------ | ------------------------------------------------------------ | ------------- |
| Thu thập ≥ 1.000 tài liệu tiếng Việt             | 2.232 bài viết từ 7 danh mục VnExpress                       | Hoàn thành    |
| Pipeline tiền xử lý NLP tiếng Việt                | Tách từ (Underthesea) + lowercase + lọc stopwords             | Hoàn thành    |
| Tự động hóa thu thập dữ liệu                     | 4 workflow n8n (daily sync, backfill, comments)               | Hoàn thành    |
| Vector hóa TF-IDF + lưu trữ Qdrant               | TfidfVectorizer 5.000 features + Qdrant cosine search         | Hoàn thành    |
| API tìm kiếm ngữ nghĩa                           | POST /api/v1/search với lọc danh mục                          | Hoàn thành    |
| Giao diện web hiện đại, responsive                | Next.js 16 + Dark Mode + 3D Hero + lịch sử tìm kiếm          | Hoàn thành    |
| Thời gian phản hồi < 500ms                        | Trung bình ~200ms                                            | Hoàn thành    |
| Tìm kiếm vector < 50ms                            | 10–50ms trên Qdrant                                          | Hoàn thành    |
| Đóng gói Docker Compose                           | 5 containers, khởi động bằng 1 lệnh                          | Hoàn thành    |

_Bảng 5.1. Tổng hợp mức độ hoàn thành các mục tiêu đề tài_

Tóm lại, đề tài đã hoàn thành **toàn bộ bốn nhóm mục tiêu** đặt ra tại Chương 1, xây dựng thành công một hệ thống truy hồi thông tin ngữ nghĩa tiếng Việt hoàn chỉnh từ khâu thu thập dữ liệu, tiền xử lý ngôn ngữ, vector hóa, đến tìm kiếm và trình bày kết quả. Hệ thống chứng minh tính khả thi của việc áp dụng VSM kết hợp TF-IDF cho bài toán tìm kiếm ngữ nghĩa trên dữ liệu tiếng Việt trong bối cảnh thực tế.

---

## 5.2. Hạn chế của hệ thống

Mặc dù đã đạt được các mục tiêu đề ra, hệ thống VnSearch Engine vẫn tồn tại một số hạn chế cần được nhận thức rõ ràng. Việc trình bày trung thực các hạn chế thể hiện tính trung thực khoa học và đồng thời định hướng cho các nghiên cứu cải tiến tiếp theo.

### 5.2.1. Hạn chế về khả năng nắm bắt ngữ nghĩa

Hạn chế lớn nhất và mang tính bản chất của hệ thống nằm ở mô hình biểu diễn TF-IDF. Là một phương pháp biểu diễn thưa (sparse representation) dựa trên khớp từ vựng (lexical matching), TF-IDF không có khả năng xử lý hai hiện tượng ngôn ngữ quan trọng [2][5]:

**Thứ nhất, hiện tượng đồng nghĩa (synonymy)**. Khi truy vấn sử dụng một thuật ngữ đồng nghĩa với thuật ngữ trong tài liệu, hệ thống không thể nhận diện mối liên hệ ngữ nghĩa giữa chúng. Cụ thể, truy vấn "AI" sẽ không tìm được bài viết chỉ chứa "trí tuệ nhân tạo" mà không có từ "AI", vì hai chuỗi ký tự này là hai token hoàn toàn khác biệt trong không gian vector TF-IDF. Tương tự, "xe hơi" và "ô tô", hay "dịch bệnh" và "đại dịch" được coi là các thuật ngữ không liên quan trong biểu diễn thưa.

**Thứ hai, hiện tượng đa nghĩa (polysemy)**. Một thuật ngữ có nhiều nghĩa khác nhau tùy ngữ cảnh được biểu diễn bằng cùng một chiều duy nhất trong vector TF-IDF. Ví dụ, từ "sao" có thể mang nghĩa thiên văn (ngôi sao), nghĩa giải trí (ngôi sao ca nhạc), hoặc nghĩa nghi vấn (tại sao), nhưng TF-IDF không phân biệt được các nghĩa này. Hạn chế này dẫn đến việc trả về một số kết quả không liên quan về mặt ngữ cảnh, mặc dù khớp về mặt từ vựng.

### 5.2.2. Hạn chế về đánh giá định lượng

Như đã nhận thức tại mục 1.3.2, đề tài chưa có bộ dữ liệu benchmark chuẩn (ground truth) cho bài toán truy hồi thông tin tiếng Việt trên dữ liệu tin tức. Do đó, việc đánh giá chất lượng truy hồi được thực hiện ở mức định tính (qualitative) thông qua kiểm tra thủ công trên một số kịch bản thử nghiệm (Chương 4), chưa thể đo lường bằng các chỉ số chuẩn như Precision@K, Recall@K, MAP (Mean Average Precision) hay NDCG (Normalized Discounted Cumulative Gain) [8]. Điều này khiến việc so sánh khách quan hiệu quả của hệ thống với các phương pháp khác (ví dụ: BM25, dense embedding) trở nên khó khăn.

### 5.2.3. Hạn chế về nguồn dữ liệu và phạm vi ngôn ngữ

Hệ thống hiện chỉ thu thập dữ liệu từ một nguồn duy nhất là VnExpress, giới hạn sự đa dạng về phong cách viết và từ vựng chuyên ngành. Ngoài ra, hệ thống chỉ hỗ trợ tốt văn bản tiếng Việt có dấu chuẩn Unicode — các truy vấn viết không dấu, viết tắt, hoặc sử dụng ngôn ngữ lóng (slang) chưa được xử lý tối ưu. Quy mô dữ liệu hiện tại (khoảng 2.200 bài viết) là đủ cho mục đích minh chứng kỹ thuật, nhưng chưa phản ánh điều kiện vận hành thực tế của một hệ thống tìm kiếm quy mô lớn với hàng trăm nghìn hoặc hàng triệu tài liệu.

### 5.2.4. Hạn chế về bảo mật và vận hành

Hệ thống được xây dựng cho mục đích nghiên cứu và học tập, chưa tích hợp các cơ chế bảo mật cần thiết cho môi trường sản xuất (production): không có xác thực người dùng (authentication), không có phân quyền (authorization), cấu hình CORS (Cross-Origin Resource Sharing) cho phép tất cả các origin, và endpoint nạp dữ liệu (`POST /api/v1/ingest`) được phơi bày công khai thay vì giới hạn cho quản trị viên. Ngoài ra, hệ thống chưa tích hợp giám sát (monitoring) và ghi nhật ký tập trung (centralized logging), gây khó khăn cho việc theo dõi và xử lý sự cố trong môi trường vận hành thực tế.

---

## 5.3. Hướng phát triển

Dựa trên các hạn chế đã phân tích, đề tài đề xuất các hướng phát triển sau nhằm nâng cao chất lượng và mở rộng phạm vi ứng dụng của hệ thống.

### 5.3.1. Nâng cao chất lượng truy hồi bằng mô hình nhúng ngữ nghĩa sâu

Hướng phát triển ưu tiên hàng đầu là tích hợp các mô hình nhúng ngữ nghĩa sâu (dense semantic embedding) để khắc phục hạn chế cốt lõi của TF-IDF trong việc xử lý đồng nghĩa và đa nghĩa. Cụ thể, mô hình PhoBERT [21] — mô hình ngôn ngữ dựa trên kiến trúc BERT được huấn luyện riêng cho tiếng Việt trên kho ngữ liệu lớn — có thể được sử dụng để sinh vector biểu diễn dày đặc (dense vector) cho tài liệu và truy vấn. Bên cạnh đó, các mô hình Sentence Transformers [22] cho phép sinh vector ở cấp độ câu, phù hợp hơn cho bài toán tìm kiếm ngữ nghĩa so với vector ở cấp độ từ.

Kiến trúc Microservices hiện tại của hệ thống đã được thiết kế với khả năng mở rộng — việc thay thế hoặc bổ sung module vector hóa TF-IDF bằng module nhúng ngữ nghĩa sâu có thể được thực hiện mà không ảnh hưởng đến các thành phần khác. Hơn nữa, phương pháp tìm kiếm lai (hybrid search) — kết hợp điểm số từ cả TF-IDF (sparse) và dense embedding — đã được chứng minh cho kết quả vượt trội so với mỗi phương pháp đơn lẻ trong nhiều nghiên cứu gần đây [23]. Qdrant hỗ trợ sẵn cơ chế lưu trữ đa vector (multi-vector) và tính toán điểm kết hợp, tạo điều kiện thuận lợi cho việc triển khai hybrid search.

### 5.3.2. Mở rộng nguồn dữ liệu và quy mô

Để nâng cao tính đa dạng và quy mô của kho ngữ liệu, hệ thống có thể mở rộng thu thập dữ liệu từ nhiều nguồn tin tức trực tuyến khác tại Việt Nam như Tuổi Trẻ (tuoitre.vn), Thanh Niên (thanhnien.vn), Dân Trí (dantri.com.vn) và các nguồn chuyên ngành. Việc mở rộng đa nguồn đặt ra yêu cầu về chuẩn hóa dữ liệu (data normalization) và loại bỏ bài viết trùng lặp xuyên nguồn (cross-source deduplication), có thể giải quyết bằng các kỹ thuật so sánh fingerprint hoặc similarity hashing.

Bên cạnh đó, việc kiểm chứng hiệu suất hệ thống trên quy mô hàng trăm nghìn tài liệu là cần thiết để đánh giá khả năng mở rộng (scalability) thực tế. Qdrant hỗ trợ chế độ phân tán (cluster mode) với khả năng phân mảnh (sharding) và sao lưu (replication), cho phép mở rộng ngang (horizontal scaling) khi khối lượng dữ liệu tăng.

### 5.3.3. Xây dựng bộ đánh giá định lượng

Để có cơ sở so sánh khách quan giữa các phương pháp, cần xây dựng bộ dữ liệu đánh giá (evaluation dataset) bao gồm: tập truy vấn mẫu (query set), tập tài liệu liên quan cho mỗi truy vấn (relevance judgments), và áp dụng các chỉ số đánh giá chuẩn trong lĩnh vực IR: Precision@K, Recall@K, MAP và NDCG [8]. Bộ đánh giá này có thể được xây dựng thông qua gán nhãn thủ công (manual annotation) bởi nhiều người đánh giá (assessors), hoặc tận dụng dữ liệu nhấp chuột (click-through data) nếu hệ thống được triển khai rộng rãi trong tương lai.

### 5.3.4. Cải thiện xử lý ngôn ngữ

Một số cải tiến ở tầng xử lý ngôn ngữ có thể nâng cao chất lượng truy hồi mà không cần thay đổi mô hình biểu diễn. **Thứ nhất**, bổ sung khả năng xử lý truy vấn không dấu bằng cách tích hợp module dự đoán dấu (accent prediction) tự động, cho phép chuyển đổi truy vấn không dấu về dạng có dấu trước khi đưa vào pipeline tìm kiếm. **Thứ hai**, mở rộng truy vấn (query expansion) bằng cách bổ sung các thuật ngữ đồng nghĩa hoặc liên quan — ví dụ: khi người dùng tìm "AI", hệ thống tự động bổ sung "trí tuệ nhân tạo" vào truy vấn, giúp cải thiện Recall mà không yêu cầu mô hình nhúng sâu. **Thứ ba**, tích hợp cơ chế gợi ý truy vấn (query suggestion) và tự động hoàn thành (autocomplete), hỗ trợ người dùng xây dựng truy vấn hiệu quả hơn.

### 5.3.5. Tăng cường bảo mật và giám sát vận hành

Để triển khai hệ thống trong môi trường sản xuất, cần bổ sung các cơ chế: xác thực API bằng khóa API (API key) hoặc JSON Web Token (JWT), hạn chế CORS cho các origin được phép, giới hạn tốc độ truy cập (rate limiting) để ngăn chặn lạm dụng, và giám sát hệ thống thông qua bộ công cụ Prometheus + Grafana kết hợp ghi nhật ký tập trung. Ngoài ra, việc thiết lập pipeline CI/CD (Continuous Integration / Continuous Deployment) bằng GitHub Actions sẽ tự động hóa quy trình kiểm thử và triển khai, giảm thiểu rủi ro lỗi khi cập nhật phiên bản mới.

### 5.3.6. Bổ sung tính năng phân tích nâng cao

Trong dài hạn, hệ thống có thể mở rộng với các tính năng phân tích nâng cao: phân tích cảm xúc (sentiment analysis) trên bình luận để đánh giá phản ứng của độc giả đối với từng bài viết, phân cụm tài liệu (document clustering) để tự động nhóm các bài viết cùng chủ đề, và tóm tắt tự động (automatic summarization) cho phép người dùng nhanh chóng nắm bắt nội dung chính mà không cần đọc toàn bộ bài viết. Những tính năng này tận dụng được hạ tầng NLP và vector database đã xây dựng, đồng thời gia tăng đáng kể giá trị sử dụng thực tế cho người dùng cuối.

---

## Tài liệu tham khảo Chương 5

[2] C. D. Manning, P. Raghavan, and H. Schütze, _Introduction to Information Retrieval_, Cambridge University Press, 2008.

[3] G. Salton, A. Wong, and C. S. Yang, "A Vector Space Model for Automatic Indexing," _Communications of the ACM_, vol. 18, no. 11, pp. 613–620, 1975.

[5] G. Salton and M. J. McGill, _Introduction to Modern Information Retrieval_, McGraw-Hill, 1983.

[8] R. Baeza-Yates and B. Ribeiro-Neto, _Modern Information Retrieval: The Concepts and Technology Behind Search_, 2nd ed., Addison-Wesley, 2011.

[12] V. T. Vu, "Underthesea — Vietnamese NLP Toolkit," _GitHub Repository_, 2017. [Trực tuyến]. Truy cập: https://github.com/undertheseanlp/underthesea

[15] F. Pedregosa _et al._, "Scikit-learn: Machine Learning in Python," _Journal of Machine Learning Research_, vol. 12, pp. 2825–2830, 2011.

[16] Qdrant Team, "Qdrant — Vector Search Engine," _Qdrant Documentation_, 2023. [Trực tuyến]. Truy cập: https://qdrant.tech/documentation/

[19] J. Nielsen, _Usability Engineering_, Academic Press, 1993.

[21] D. Q. Nguyen and A. T. Nguyen, "PhoBERT: Pre-trained Language Models for Vietnamese," _Findings of the Association for Computational Linguistics: EMNLP 2020_, pp. 1037–1042, 2020.

[22] N. Reimers and I. Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks," _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pp. 3982–3992, 2019.

[23] S. Luan, S. Ai, C. Wang, and Y. Cheng, "Sparse, Dense, and Attentional Representations for Text Retrieval," _Transactions of the Association for Computational Linguistics_, vol. 9, pp. 329–345, 2021.

> **Ghi chú**: Tài liệu [2], [3], [5], [8] đã được giới thiệu ở Chương 1 và Chương 2; tài liệu [12], [15], [16] đã được giới thiệu ở Chương 2; tài liệu [19] đã được giới thiệu ở Chương 4. Các tài liệu này được trích dẫn lại ở Chương 5 với cùng số thứ tự để đảm bảo tính nhất quán. Tài liệu mới của Chương 5 là [21], [22], [23].
