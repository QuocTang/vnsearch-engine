# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

Chương này trình bày nền tảng lý thuyết phục vụ cho việc thiết kế và xây dựng hệ thống truy hồi thông tin tiếng Việt của đề tài. Các nội dung bao gồm: tổng quan về hệ truy hồi thông tin, các kỹ thuật xử lý ngôn ngữ tự nhiên cho tiếng Việt, sơ đồ trọng số TF-IDF, mô hình Không gian Vector, và cơ chế chỉ mục tài liệu. Mỗi khái niệm được trình bày kèm theo cơ sở toán học và ý nghĩa ứng dụng trong bối cảnh đề tài.

---

## 2.1. Tổng quan về Hệ truy hồi thông tin (Information Retrieval — IR)

Truy hồi thông tin (Information Retrieval — IR) đã được giới thiệu ở Chương 1 như lĩnh vực nghiên cứu về các phương pháp tìm kiếm, trích xuất và xếp hạng tài liệu từ một tập hợp lớn dựa trên nhu cầu thông tin của người dùng [2]. Mục này đi sâu hơn vào các thành phần kiến trúc cơ bản mà một hệ thống IR hoàn chỉnh cần có, nhằm tạo nền tảng cho việc thiết kế hệ thống trong các chương tiếp theo.

### 2.1.1. Định nghĩa hình thức

Một cách hình thức, bài toán IR có thể được phát biểu như sau: cho một tập hợp tài liệu $D = \{d_1, d_2, ..., d_n\}$ và một truy vấn $q$ biểu diễn nhu cầu thông tin của người dùng, hệ thống IR cần xác định một hàm xếp hạng $f(q, d_i) \rightarrow \mathbb{R}$ sao cho giá trị $f$ phản ánh mức độ liên quan (relevance) giữa truy vấn $q$ và tài liệu $d_i$ [8]. Tập kết quả trả về $R \subseteq D$ bao gồm các tài liệu có giá trị $f$ cao nhất, được sắp xếp theo thứ tự giảm dần. Đây là bài toán xếp hạng (ranking problem), khác biệt cơ bản so với bài toán tìm kiếm chính xác (exact matching) trong các hệ quản trị cơ sở dữ liệu truyền thống.

Hiệu quả của hệ thống IR được đánh giá thông qua hai tiêu chí chính: **độ chính xác (Precision)** — tỷ lệ tài liệu liên quan trong số các tài liệu được trả về — và **độ phủ (Recall)** — tỷ lệ tài liệu liên quan được truy hồi so với tổng số tài liệu liên quan trong toàn bộ tập hợp. Hai tiêu chí này thường có mối quan hệ đánh đổi (trade-off): việc tăng số lượng kết quả trả về có thể cải thiện Recall nhưng làm giảm Precision, và ngược lại [2].

### 2.1.2. Các thành phần cơ bản của hệ thống IR

Một hệ thống IR hoàn chỉnh bao gồm các thành phần cốt lõi sau [8][2]:

**Thứ nhất, module thu thập tài liệu (Document Acquisition)**. Thành phần này chịu trách nhiệm thu thập dữ liệu đầu vào từ các nguồn khác nhau — có thể là các tệp tin cục bộ, cơ sở dữ liệu, hoặc nội dung được thu thập tự động từ web (web crawling). Dữ liệu đầu vào thường ở dạng phi cấu trúc (unstructured data), đặc biệt là văn bản tự nhiên, và cần được chuẩn hóa trước khi đưa vào các bước xử lý tiếp theo. Trong bối cảnh đề tài, thành phần này tương ứng với Crawler thu thập bài báo từ VnExpress.

**Thứ hai, module tiền xử lý văn bản (Text Preprocessing)**. Sau khi được thu thập, văn bản cần trải qua một chuỗi các bước tiền xử lý nhằm chuẩn hóa và trích xuất các đặc trưng có ý nghĩa. Các bước phổ biến bao gồm: tách từ (tokenization/word segmentation), chuẩn hóa chữ hoa-chữ thường (case normalization), loại bỏ từ dừng (stopword removal), và trong một số trường hợp, bổ sung các kỹ thuật như stemming hoặc lemmatization. Đối với tiếng Việt, bước tách từ mang tính chất đặc biệt quan trọng do đặc thù ngôn ngữ đơn lập, như đã phân tích ở mục 1.1.3 của Chương 1.

**Thứ ba, module đánh chỉ mục (Indexing)**. Đây là thành phần then chốt quyết định hiệu suất truy hồi. Mục tiêu của đánh chỉ mục là tổ chức tài liệu đã qua tiền xử lý thành một cấu trúc dữ liệu cho phép truy vấn nhanh. Cấu trúc được sử dụng phổ biến nhất là Chỉ mục đảo ngược (Inverted Index), trong đó mỗi thuật ngữ ánh xạ đến danh sách các tài liệu chứa nó [8]. Bên cạnh đó, với sự phát triển của các phương pháp biểu diễn dạng vector, các cơ sở dữ liệu vector chuyên dụng (Vector Database) cũng ngày càng được sử dụng rộng rãi cho mục đích này.

**Thứ tư, module tìm kiếm và xếp hạng (Search & Ranking)**. Khi nhận được truy vấn từ người dùng, hệ thống áp dụng cùng pipeline tiền xử lý cho truy vấn (đảm bảo tính nhất quán), sau đó sử dụng hàm xếp hạng để tính toán mức độ liên quan giữa truy vấn và các tài liệu trong chỉ mục. Kết quả được trả về theo thứ tự giảm dần của điểm tương đồng (relevance score).

**Thứ năm, module trình bày kết quả (Result Presentation)**. Thành phần cuối cùng chịu trách nhiệm hiển thị kết quả cho người dùng một cách trực quan, bao gồm các thông tin như tiêu đề, tóm tắt nội dung, điểm số tương đồng, và các metadata liên quan. Giao diện trình bày ảnh hưởng trực tiếp đến trải nghiệm người dùng và hiệu quả sử dụng thực tế của hệ thống.

---

## 2.2. Xử lý ngôn ngữ tự nhiên (NLP) cho tiếng Việt

Xử lý Ngôn ngữ Tự nhiên (Natural Language Processing — NLP) là lĩnh vực nghiên cứu tại giao thoa giữa Khoa học Máy tính và Ngôn ngữ học, tập trung vào việc phát triển các phương pháp cho phép máy tính hiểu, phân tích và sinh ra ngôn ngữ tự nhiên của con người [9]. Trong bối cảnh hệ thống IR, NLP đóng vai trò nền tảng ở khâu tiền xử lý — chuyển đổi văn bản thô thành dạng biểu diễn phù hợp cho các mô hình tính toán.

Đối với tiếng Việt, các kỹ thuật NLP cần được điều chỉnh để phù hợp với đặc thù ngôn ngữ đơn lập (isolating language). Mục này trình bày hai vấn đề cốt lõi: bài toán tách từ và xử lý từ dừng.

### 2.2.1. Bài toán tách từ tiếng Việt và các công cụ hỗ trợ

#### Đặc thù tách từ tiếng Việt

Như đã trình bày ở mục 1.1.3, tiếng Việt là ngôn ngữ đơn lập — các đơn vị từ vựng (từ) có thể bao gồm một hoặc nhiều âm tiết (syllable) được phân tách bằng khoảng trắng [7]. Điều này tạo ra sự nhập nhằng (ambiguity) mà bài toán tách từ (word segmentation) cần giải quyết. Cụ thể, chuỗi ký tự "học sinh học sinh học" có thể được tách thành "học_sinh / học / sinh_học" hoặc "học / sinh_học / sinh_học", mỗi cách tách mang ý nghĩa hoàn toàn khác biệt.

Bài toán tách từ tiếng Việt được xem là bước tiền xử lý bắt buộc (mandatory preprocessing step) trong mọi hệ thống NLP và IR cho tiếng Việt [10]. Chất lượng tách từ ảnh hưởng trực tiếp đến toàn bộ pipeline phía sau — nếu tách sai, vector biểu diễn tài liệu và truy vấn sẽ sai lệch, dẫn đến kết quả truy hồi không chính xác.

#### Các phương pháp và công cụ

Trong lịch sử phát triển, nhiều công cụ tách từ tiếng Việt đã được đề xuất, có thể phân thành ba nhóm phương pháp chính [10][11]:

**Thứ nhất, phương pháp dựa trên từ điển (Dictionary-based)**. Phương pháp này sử dụng một từ điển tiếng Việt đã được xây dựng sẵn để đối chiếu và xác định ranh giới từ trong văn bản. Thuật toán khớp dài nhất (longest matching) là kỹ thuật phổ biến nhất trong nhóm này — thuật toán quét văn bản từ trái sang phải, tại mỗi vị trí tìm chuỗi con dài nhất khớp với một mục trong từ điển. Ưu điểm của phương pháp này là đơn giản và nhanh, tuy nhiên nhược điểm lớn nhất là không xử lý được các từ ngoài từ điển (out-of-vocabulary — OOV) và các trường hợp nhập nhằng.

**Thứ hai, phương pháp dựa trên thống kê và học máy (Statistical/Machine Learning)**. Nhóm phương pháp này mô hình hóa bài toán tách từ như một bài toán gán nhãn chuỗi (sequence labeling), trong đó mỗi âm tiết được gán một nhãn cho biết nó là đầu từ (B — Begin), giữa từ (I — Inside) hay một từ đơn (S — Single). Các mô hình phổ biến bao gồm Trường ngẫu nhiên có điều kiện (Conditional Random Fields — CRF), Máy vector hỗ trợ (Support Vector Machine — SVM), và Mạng nơ-ron hồi quy (Recurrent Neural Network — RNN) [11]. **JvnTextPro** là một công cụ tiêu biểu sử dụng mô hình Entropy cực đại (Maximum Entropy) kết hợp CRF cho tách từ tiếng Việt, được phát triển bởi Nguyen và cộng sự [10].

**Thứ ba, phương pháp kết hợp (Hybrid)**. Phương pháp này tích hợp cả tri thức từ điển và mô hình thống kê để tận dụng ưu điểm của cả hai hướng tiếp cận. **VnTokenizer** là ví dụ điển hình — sử dụng tập luật ngữ pháp kết hợp với mô hình xác suất để giải quyết nhập nhằng [7]. Tương tự, **Underthesea** là một thư viện NLP mã nguồn mở (open-source) hiện đại cho tiếng Việt, cung cấp chức năng tách từ dựa trên mô hình học sâu (deep learning), được huấn luyện trên tập dữ liệu gán nhãn lớn [12]. Underthesea hỗ trợ nhiều tác vụ NLP khác ngoài tách từ, bao gồm nhận dạng thực thể (Named Entity Recognition — NER), phân loại văn bản (text classification) và phân tích cảm xúc (sentiment analysis).

Bảng 2.1 dưới đây tổng hợp so sánh các công cụ tách từ tiếng Việt phổ biến:

| **Công cụ** | **Phương pháp**            | **Ngôn ngữ lập trình** | **Ưu điểm**                                      | **Hạn chế**                         |
| ----------- | -------------------------- | ---------------------- | ------------------------------------------------ | ----------------------------------- |
| JvnTextPro  | MaxEnt + CRF               | Java                   | Độ chính xác cao trên dữ liệu chuẩn              | Tốc độ chậm, cần JVM                |
| VnTokenizer | Hybrid (Luật + Xác suất)   | Java                   | Xử lý tốt nhập nhằng                             | Không còn được bảo trì tích cực     |
| VnCoreNLP   | CRF + Neural Network       | Java                   | Đa tác vụ, hiệu suất cao                         | Yêu cầu tài nguyên lớn              |
| Underthesea | Deep Learning (BiLSTM-CRF) | Python                 | Dễ tích hợp, API đơn giản, cập nhật thường xuyên | Tốc độ phụ thuộc kích thước mô hình |
| PyVi        | Regex + Dictionary         | Python                 | Nhẹ, nhanh                                       | Độ chính xác hạn chế                |

_Bảng 2.1. So sánh các công cụ tách từ tiếng Việt phổ biến_

Trong đề tài này, thư viện **Underthesea** được lựa chọn làm công cụ tách từ chính vì ba lý do: (i) hỗ trợ nguyên bản Python — ngôn ngữ lập trình chính của backend hệ thống; (ii) cung cấp API đơn giản, dễ tích hợp vào pipeline tiền xử lý; và (iii) được cộng đồng duy trì và cập nhật thường xuyên với mô hình huấn luyện trên tập dữ liệu hiện đại.

### 2.2.2. Xử lý từ dừng (Stopwords) trong tiếng Việt

#### Khái niệm từ dừng

Từ dừng (stopwords) là các từ xuất hiện với tần suất rất cao trong hầu hết các văn bản nhưng mang rất ít hoặc không mang giá trị ngữ nghĩa phân biệt (discriminative value) cho bài toán truy hồi thông tin [2][8]. Trong tiếng Anh, các từ dừng điển hình bao gồm "the", "is", "at", "which", "on". Đối với tiếng Việt, danh sách từ dừng bao gồm các từ chức năng (function words) như "và", "của", "là", "những", "các", "thì", "đã", "sẽ", "cũng", "nhưng".

Việc loại bỏ từ dừng mang lại hai lợi ích chính. **Thứ nhất**, về mặt chất lượng truy hồi: các từ dừng có tần suất xuất hiện cao trong toàn bộ tập tài liệu, do đó giá trị IDF của chúng rất thấp; tuy nhiên, sự hiện diện của chúng vẫn tạo nhiễu cho vector biểu diễn, làm giảm khả năng phân biệt giữa các tài liệu. Loại bỏ chúng giúp vector biểu diễn tập trung hơn vào các thuật ngữ mang nội dung (content words). **Thứ hai**, về mặt hiệu suất tính toán: loại bỏ từ dừng làm giảm đáng kể kích thước không gian đặc trưng (feature space), từ đó giảm chi phí lưu trữ và tăng tốc quá trình tính toán vector cũng như tìm kiếm tương đồng.

#### Xây dựng danh sách từ dừng tiếng Việt

Khác với tiếng Anh — nơi các danh sách từ dừng đã được chuẩn hóa và tích hợp sẵn trong các thư viện NLP phổ biến như NLTK và spaCy — tiếng Việt chưa có một danh sách từ dừng chuẩn được thống nhất rộng rãi. Các danh sách hiện có thường được xây dựng dựa trên ba phương pháp: (i) phương pháp thủ công bởi chuyên gia ngôn ngữ học; (ii) phương pháp tự động dựa trên ngưỡng tần suất (frequency threshold) — loại bỏ các từ có tần suất xuất hiện vượt quá một ngưỡng nhất định trong tập tài liệu; và (iii) phương pháp kết hợp, sử dụng danh sách cơ sở từ chuyên gia và bổ sung bằng phân tích thống kê trên tập dữ liệu cụ thể [13].

Trong đề tài này, hệ thống sử dụng một danh sách từ dừng tiếng Việt chuyên dụng được lưu trữ dưới dạng tệp văn bản (plain text), mỗi dòng chứa một từ dừng. Danh sách này được nạp vào bộ nhớ và lưu trữ dưới dạng tập hợp (set) để đảm bảo thời gian tra cứu $O(1)$ cho mỗi thao tác kiểm tra. Quá trình loại bỏ từ dừng được thực hiện sau bước tách từ và chuẩn hóa chữ thường (lowercasing), đảm bảo tính nhất quán trong toàn bộ pipeline tiền xử lý.

---

## 2.3. Trọng số TF-IDF

### 2.3.1. Khái niệm và động lực

Trong mô hình Không gian Vector (Vector Space Model — VSM), mỗi tài liệu và truy vấn được biểu diễn dưới dạng vector trong không gian nhiều chiều, trong đó mỗi chiều tương ứng với một thuật ngữ (term) trong từ điển (vocabulary) của tập tài liệu. Câu hỏi cốt lõi là: giá trị tại mỗi chiều — tức trọng số (weight) của thuật ngữ — nên được tính toán như thế nào để phản ánh đúng tầm quan trọng của thuật ngữ đối với tài liệu?

Sơ đồ trọng số TF-IDF (Term Frequency — Inverse Document Frequency) được đề xuất bởi Sparck Jones (1972) [6] và phát triển bởi Salton và Buckley (1988) [14] là phương pháp gán trọng số được sử dụng phổ biến nhất trong lĩnh vực IR. Ý tưởng trung tâm của TF-IDF dựa trên hai quan sát thực nghiệm:

- Một thuật ngữ xuất hiện **nhiều lần** trong một tài liệu thì có khả năng **quan trọng** đối với nội dung tài liệu đó (yếu tố TF).
- Một thuật ngữ xuất hiện trong **ít tài liệu** thì có khả năng **phân biệt** (discriminative) tốt hơn — tức có giá trị cao hơn trong việc phân biệt tài liệu liên quan và không liên quan (yếu tố IDF).

### 2.3.2. Công thức toán học

#### Tần suất thuật ngữ — Term Frequency (TF)

Tần suất thuật ngữ $\text{TF}(t, d)$ đo lường mức độ xuất hiện của thuật ngữ $t$ trong tài liệu $d$. Có nhiều biến thể của TF, trong đó phổ biến nhất bao gồm [2]:

- **TF thô (Raw TF)**:

$$\text{TF}(t, d) = f_{t,d}$$

Đơn giản là số lần thuật ngữ $t$ xuất hiện trong tài liệu $d$.

- **TF chuẩn hóa logarit (Logarithmic TF)**:

$$\text{TF}(t, d) = \begin{cases} 1 + \log(f_{t,d}) & \text{nếu } f_{t,d} > 0 \\ 0 & \text{ngược lại} \end{cases}$$

Biến thể này giảm thiểu ảnh hưởng của các thuật ngữ có tần suất quá cao bằng cách nén giá trị theo hàm logarit.

Biến thể logarit được ưu tiên trong thực tế vì nó phản ánh tốt hơn mối quan hệ giữa tần suất xuất hiện và tầm quan trọng — sự khác biệt giữa một thuật ngữ xuất hiện 1 lần và 10 lần có ý nghĩa hơn nhiều so với sự khác biệt giữa 100 lần và 110 lần.

#### Tần suất nghịch đảo tài liệu — Inverse Document Frequency (IDF)

Tần suất nghịch đảo tài liệu $\text{IDF}(t)$ đo lường mức độ phổ biến (hoặc hiếm) của thuật ngữ $t$ trong toàn bộ tập tài liệu. Công thức chuẩn được định nghĩa như sau [6]:

$$\text{IDF}(t, D) = \log \left( \frac{N}{df(t)} \right)$$

Trong đó:

- $N$ — tổng số tài liệu trong tập hợp.
- $df(t)$ — số tài liệu chứa thuật ngữ $t$ (document frequency).

> **Lưu ý:** Trong triển khai thực tế, người ta thường cộng 1 vào mẫu số: $\text{IDF}(t) = \log\left(\frac{N}{1 + df(t)}\right)$ để tránh lỗi chia cho 0 nếu thuật ngữ chưa từng xuất hiện.

Giá trị IDF cao khi thuật ngữ chỉ xuất hiện trong ít tài liệu (hiếm, có tính phân biệt cao), và thấp khi thuật ngữ xuất hiện trong nhiều tài liệu (phổ biến, ít giá trị phân biệt). Các từ dừng có $df(t)$ gần bằng $N$, do đó $\text{IDF}$ gần bằng 0, phản ánh đúng bản chất không mang giá trị phân biệt của chúng.

#### Trọng số TF-IDF tổng hợp

Trọng số TF-IDF của thuật ngữ $t$ trong tài liệu $d$ được tính bằng tích của hai thành phần [6][14]:

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Giá trị $\text{TF-IDF}(t, d)$ cao khi thuật ngữ $t$ vừa xuất hiện thường xuyên trong tài liệu $d$ (TF cao), vừa hiếm trong toàn bộ tập tài liệu (IDF cao). Ngược lại, giá trị này thấp khi thuật ngữ hoặc hiếm trong tài liệu $d$ hoặc quá phổ biến trong toàn bộ tập hợp. Sự kết hợp này đảm bảo rằng các thuật ngữ có khả năng phân biệt cao nhất giữa các tài liệu sẽ nhận được trọng số lớn nhất.

### 2.3.3. Ý nghĩa và ưu điểm

Sơ đồ trọng số TF-IDF mang lại một số ý nghĩa quan trọng trong thực tiễn. **Thứ nhất**, TF-IDF cung cấp một cơ chế **tự động đánh giá tầm quan trọng** của thuật ngữ mà không cần tri thức chuyên gia — hệ thống tự học từ phân bố thống kê của dữ liệu. **Thứ hai**, TF-IDF có **tính khả diễn giải (interpretability) cao** — trọng số của mỗi thuật ngữ có ý nghĩa thống kê rõ ràng, cho phép giải thích tại sao một tài liệu được xếp hạng cao cho một truy vấn cụ thể [8]. **Thứ ba**, TF-IDF có **chi phí tính toán thấp** — chỉ yêu cầu các phép toán đếm và logarit, không cần tài nguyên GPU hay quá trình huấn luyện phức tạp như các mô hình nhúng ngữ nghĩa sâu (deep semantic embedding).

---

## 2.4. Mô hình Không gian Vector (Vector Space Model — VSM)

### 2.4.1. Cách biểu diễn văn bản dưới dạng vector

Mô hình Không gian Vector (Vector Space Model — VSM) được đề xuất bởi Salton, Wong và Yang (1975) [3] là một trong những mô hình biểu diễn tài liệu quan trọng nhất trong lịch sử IR. Ý tưởng cốt lõi của VSM là biểu diễn cả tài liệu và truy vấn dưới dạng các vector trong một không gian Euclid nhiều chiều, trong đó mỗi chiều tương ứng với một thuật ngữ duy nhất (unique term) trong từ điển.

Cho từ điển $V = \{t_1, t_2, ..., t_m\}$ gồm $m$ thuật ngữ duy nhất được trích xuất từ toàn bộ tập tài liệu $D$, mỗi tài liệu $d_j$ được biểu diễn bằng một vector $m$ chiều [3][5]:

$$\vec{d_j} = (w_{1,j},\ w_{2,j},\ ...,\ w_{m,j})$$

Trong đó $w_{i,j}$ là trọng số của thuật ngữ $t_i$ trong tài liệu $d_j$, được tính theo sơ đồ TF-IDF như đã trình bày ở mục 2.3. Tương tự, truy vấn $q$ cũng được biểu diễn dưới dạng vector trong cùng không gian:

$$\vec{q} = (w_{1,q},\ w_{2,q},\ ...,\ w_{m,q})$$

Quá trình biểu diễn này được gọi là **vector hóa (vectorization)** — chuyển đổi từ biểu diễn ngôn ngữ tự nhiên (ký tự, từ) sang biểu diễn số học (vector) mà máy tính có thể xử lý và so sánh. Trong triển khai thực tế, thư viện Scikit-learn cung cấp lớp `TfidfVectorizer` cho phép thực hiện đồng thời quá trình xây dựng từ điển, tính toán trọng số TF-IDF và sinh vector biểu diễn cho toàn bộ tập tài liệu [15].

Một điểm quan trọng cần lưu ý: vector TF-IDF thuộc loại **vector thưa (sparse vector)** — phần lớn các thành phần có giá trị bằng 0 vì mỗi tài liệu thường chỉ chứa một tập con nhỏ của từ điển. Đặc tính này có ý nghĩa quan trọng trong việc lựa chọn cấu trúc lưu trữ và thuật toán tìm kiếm.

### 2.4.2. Độ đo tương đồng — Cosine Similarity

Sau khi tài liệu và truy vấn đã được biểu diễn dưới dạng vector, bước tiếp theo là đo lường mức độ tương đồng (similarity) giữa chúng. Trong mô hình VSM, **độ tương đồng cosine (Cosine Similarity)** là phương pháp đo phổ biến nhất [3][2].

Cosine Similarity đo góc giữa hai vector trong không gian nhiều chiều, bất kể độ lớn (magnitude) của chúng. Công thức được định nghĩa như sau:

$$\cos(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \times \|\vec{d}\|} = \frac{\sum_{i=1}^{m} w_{i,q} \times w_{i,d}}{\sqrt{\sum_{i=1}^{m} w_{i,q}^2} \times \sqrt{\sum_{i=1}^{m} w_{i,d}^2}}$$

Trong đó:

- $\vec{q} \cdot \vec{d}$ — tích vô hướng (dot product) giữa vector truy vấn và vector tài liệu.
- $\|\vec{q}\|$ và $\|\vec{d}\|$ — chuẩn Euclid ($L_2$ norm) của hai vector.

Giá trị Cosine Similarity nằm trong khoảng $[0, 1]$ (khi các trọng số không âm, điều đúng với TF-IDF). Giá trị 1 cho biết hai vector hoàn toàn cùng hướng (tài liệu hoàn toàn phù hợp với truy vấn), trong khi giá trị 0 cho biết hai vector vuông góc (không có thuật ngữ chung). Ưu điểm vượt trội của Cosine Similarity so với các phương pháp đo khác như khoảng cách Euclid (Euclidean Distance) là tính bất biến đối với độ dài tài liệu — một tài liệu dài hơn không tự động nhận điểm số cao hơn chỉ vì chứa nhiều thuật ngữ hơn [2].

Trong bối cảnh ứng dụng thực tế, cơ sở dữ liệu vector Qdrant — được sử dụng trong đề tài — hỗ trợ nguyên bản Cosine Similarity như một metric khoảng cách (distance metric), cho phép thực hiện tìm kiếm tương đồng trên hàng nghìn đến hàng triệu vector với thời gian phản hồi ở mức mili-giây nhờ các thuật toán tìm kiếm láng giềng gần đúng (Approximate Nearest Neighbor — ANN) [16].

---

## 2.5. Cơ chế chỉ mục (Indexing)

### 2.5.1. Vai trò của chỉ mục trong hệ thống IR

Chỉ mục (index) là cấu trúc dữ liệu cho phép hệ thống IR truy xuất tài liệu một cách hiệu quả mà không cần duyệt tuần tự (sequential scan) toàn bộ tập hợp [8]. Nếu không có chỉ mục, mỗi truy vấn sẽ yêu cầu tính toán mức độ tương đồng với từng tài liệu — một quá trình có độ phức tạp $O(N)$ với $N$ là số lượng tài liệu, không khả thi với các tập dữ liệu quy mô lớn. Chỉ mục giúp giảm không gian tìm kiếm, đưa thời gian truy vấn về mức chấp nhận được ngay cả khi tập dữ liệu rất lớn.

### 2.5.2. Chỉ mục đảo ngược (Inverted Index)

Chỉ mục đảo ngược (Inverted Index) là cấu trúc dữ liệu kinh điển nhất trong lĩnh vực IR, được sử dụng rộng rãi trong các hệ thống tìm kiếm thương mại như Google Search, Elasticsearch và Apache Lucene [8][2]. Cấu trúc này bao gồm hai thành phần:

- **Từ điển (Dictionary/Lexicon)**: Danh sách tất cả các thuật ngữ duy nhất trong tập tài liệu, thường được lưu trữ dưới dạng bảng băm (hash table) hoặc cây B (B-tree) để hỗ trợ tra cứu nhanh.
- **Danh sách đăng (Posting List)**: Mỗi thuật ngữ trong từ điển được ánh xạ đến một danh sách các tài liệu chứa nó, kèm theo thông tin bổ sung như tần suất xuất hiện, vị trí xuất hiện trong tài liệu.

Ví dụ, với ba tài liệu: $d_1$ = "học sinh giỏi", $d_2$ = "sinh viên giỏi", $d_3$ = "học sinh", chỉ mục đảo ngược sẽ có dạng:

| **Thuật ngữ** | **Posting List** |
| ------------- | ---------------- |
| học           | $d_1, d_3$       |
| sinh          | $d_1, d_2, d_3$  |
| giỏi          | $d_1, d_2$       |
| viên          | $d_2$            |

Khi nhận truy vấn "sinh giỏi", hệ thống tra cứu posting list của "sinh" ($d_1, d_2, d_3$) và "giỏi" ($d_1, d_2$), thực hiện phép giao (intersection) và tính điểm tương đồng chỉ trên tập $\{d_1, d_2\}$ — giảm đáng kể số lượng phép tính so với duyệt toàn bộ tập tài liệu.

### 2.5.3. Cơ sở dữ liệu vector (Vector Database)

Với sự phát triển của các phương pháp biểu diễn tài liệu dưới dạng vector (bao gồm cả TF-IDF và các phương pháp nhúng ngữ nghĩa sâu), một loại cơ sở dữ liệu chuyên dụng đã ra đời — **Cơ sở dữ liệu vector (Vector Database)** [16]. Khác với Inverted Index hoạt động trên khớp từ, Vector Database lưu trữ và tìm kiếm trên biểu diễn vector, cho phép thực hiện truy vấn dựa trên độ tương đồng hình học trong không gian nhiều chiều.

Thách thức cốt lõi của tìm kiếm vector là bài toán **Tìm kiếm Láng giềng Gần nhất (Nearest Neighbor Search — NNS)**: trong không gian $m$ chiều, tìm $k$ vector gần nhất với vector truy vấn theo một metric khoảng cách cho trước (Cosine, Euclidean, Dot Product). Giải pháp chính xác (exact search) có độ phức tạp $O(N \times m)$, không khả thi với dữ liệu lớn. Do đó, các Vector Database hiện đại sử dụng thuật toán **Tìm kiếm Láng giềng Gần đúng (Approximate Nearest Neighbor — ANN)**, chấp nhận hy sinh một lượng nhỏ độ chính xác để đạt tốc độ truy vấn nhanh hơn nhiều bậc [16].

Các thuật toán ANN phổ biến bao gồm:

- **HNSW (Hierarchical Navigable Small World)**: Xây dựng đồ thị phân tầng nhiều lớp, cho phép tìm kiếm nhanh bằng cách duyệt từ lớp thưa nhất (tổng quan) đến lớp dày nhất (chi tiết). Đây là thuật toán được Qdrant sử dụng mặc định [16].
- **IVF (Inverted File Index)**: Phân vùng không gian vector thành các cụm (cluster), chỉ tìm kiếm trong các cụm gần nhất với vector truy vấn.
- **PQ (Product Quantization)**: Nén vector bằng cách chia vector thành các sub-vector và lượng tử hóa mỗi phần, giảm bộ nhớ lưu trữ.

**Qdrant** — cơ sở dữ liệu vector được sử dụng trong đề tài — là một Vector Database mã nguồn mở, hiệu suất cao, được viết bằng ngôn ngữ Rust [16]. Qdrant hỗ trợ đầy đủ các tính năng cần thiết cho hệ thống IR: lưu trữ vector kèm metadata (payload), tìm kiếm tương đồng với nhiều metric khoảng cách (Cosine, Dot Product, Euclidean), lọc kết quả theo payload (filtering), và hỗ trợ cả giao thức HTTP lẫn gRPC. Với thuật toán HNSW tích hợp sẵn, Qdrant cung cấp thời gian truy vấn ở mức mili-giây ngay cả trên tập dữ liệu hàng triệu vector.

---

## Tài liệu tham khảo Chương 2

[8] R. Baeza-Yates and B. Ribeiro-Neto, _Modern Information Retrieval: The Concepts and Technology Behind Search_, 2nd ed., Addison-Wesley, 2011.

[9] D. Jurafsky and J. H. Martin, _Speech and Language Processing_, 3rd ed. draft, Stanford University, 2023.

[10] N. T. Phuong, N. V. Hai, and L. H. Phuong, "Vietnamese Text Processing Tools," _Proceedings of the IEEE RIVF International Conference on Computing and Communication Technologies_, pp. 51–56, 2008.

[11] L. H. Phuong, N. T. M. Huyen, R. Azim, and H. T. Vinh, "A Hybrid Approach to Word Segmentation of Vietnamese Texts," _Proceedings of the 2nd International Conference on Language and Automata Theory and Applications (LATA)_, Lecture Notes in Computer Science, vol. 5196, pp. 240–249, 2008.

[12] V. T. Vu, "Underthesea — Vietnamese NLP Toolkit," _GitHub Repository_, 2017. [Trực tuyến]. Truy cập: https://github.com/undertheseanlp/underthesea

[13] H. T. Nguyen and T. M. H. Nguyen, "Vietnamese Stopword Removal for Text Classification," _Journal of Computer Science and Cybernetics_, vol. 29, no. 2, pp. 145–157, 2013.

[14] G. Salton and C. Buckley, "Term-Weighting Approaches in Automatic Text Retrieval," _Information Processing & Management_, vol. 24, no. 5, pp. 513–523, 1988.

[15] F. Pedregosa _et al._, "Scikit-learn: Machine Learning in Python," _Journal of Machine Learning Research_, vol. 12, pp. 2825–2830, 2011.

[16] Qdrant Team, "Qdrant — Vector Search Engine," _Qdrant Documentation_, 2023. [Trực tuyến]. Truy cập: https://qdrant.tech/documentation/

> **Ghi chú**: Tài liệu [2] (Manning et al., 2008), [3] (Salton et al., 1975), [5] (Salton & McGill, 1983), [6] (Sparck Jones, 1972), và [7] (Nguyen et al., 2008) đã được giới thiệu ở Chương 1 và được trích dẫn lại ở Chương 2 với cùng số thứ tự để đảm bảo tính nhất quán. Các tài liệu mới của Chương 2 bắt đầu từ [8] đến [16].
