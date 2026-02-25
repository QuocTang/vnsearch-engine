# Độ Đo Cosine Similarity (Cosine Similarity Metric)

## 1. Giới Thiệu Chung

**Cosine Similarity** (Độ tương đồng Cosine) là một độ đo toán học được sử dụng rộng rãi trong học máy (Machine Learning) và xử lý ngôn ngữ tự nhiên (NLP) để đo lường mức độ giống nhau giữa hai chuỗi số học (được gọi là **Vector**).

Khi bạn dùng thuật toán **TF-IDF** hoặc **Word Embedding** (như Word2Vec, BERT) để biến đổi các đoạn văn bản thành các Vector chứa rất nhiều con số, làm sao để biết văn bản A có nội dung giống văn bản B hay không? Hay làm sao để biết câu "Tài liệu học thuật" (câu truy vấn của người dùng) nằm gần với bài viết nào nhất trong cơ sở dữ liệu hàng triệu bài?

Đây là lúc ta sử dụng **Cosine Similarity**.

Thay vì đo khoảng cách độ dài vật lý giữa 2 điểm (như khoảng cách Euclidean), **Cosine Similarity đo góc lệch giữa 2 Vector đó** trong không gian đa chiều.

- Nếu 2 Vector có hướng **chỉ về cùng một phía** (góc 0 độ), chúng hoàn toàn giống nhau về mặt ý nghĩa/ngữ nghĩa $\rightarrow$ Giá trị lớn nhất $= 1$.
- Nếu 2 Vector tạo thành **góc vuông** (90 độ), chúng hoàn toàn độc lập, không liên quan đến nhau $\rightarrow$ Giá trị bằng $= 0$.
- Nếu 2 Vector **ngược hướng hoàn toàn** (180 độ), chúng hoàn toàn đối lập nhau (thường ít gặp trong NLP đếm từ trường hợp TF-IDF vì từ đếm không bao giờ âm) $\rightarrow$ Giá trị nhỏ nhất $= -1$.

---

## 2. Nền Tảng Toán Học

Công thức tính độ tương đồng Cosine giữa hai Vector $\mathbf{A}$ và $\mathbf{B}$ chính là phép chia giữa **Tích vô hướng** (Dot Product) của chúng cho **Tích độ lớn** (Magnitude / Euclidean Norm) của từng Vector.

$$ \text{Cosine Similarity}(\mathbf{A}, \mathbf{B}) = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} $$

Trong đó:
Tính **Tích vô hướng (Dot Product - tử số)**: Là tổng các tích của từng cặp phần tử tương ứng:
$$ \mathbf{A} \cdot \mathbf{B} = \sum\_{i=1}^{n} {A_i B_i} = A_1 B_1 + A_2 B_2 + \dots + A_n B_n $$

Tính **Độ lớn (Magnitude - mẫu số)**: Là căn bậc hai của tổng bình phương tất cả các chiều:
$$ \|\mathbf{A}\| = \sqrt{\sum*{i=1}^{n} A_i^2} = \sqrt{A_1^2 + A_2^2 + \dots + A_n^2} $$
$$ \|\mathbf{B}\| = \sqrt{\sum*{i=1}^{n} B_i^2} = \sqrt{B_1^2 + B_2^2 + \dots + B_n^2} $$

_Ghi chú: $n$ là số chiều của vector (tương ứng với số lượng "từ vựng" trong từ điển của toàn bộ hệ thống TF-IDF)._

---

## 3. Ví Dụ Minh Hoạ Toàn Diện (Example)

Giả sử sau bước chạy thuật toán TF-IDF, hệ thống quy định bộ từ điển (vocabulary) của bạn chỉ gồm 3 từ khóa quan trọng và đánh tọa độ theo đúng thứ tự 3 từ đó: **[ Máy, Tính, Apple ]**.

Bây giờ ta có 3 văn bản và tương đương với 3 Vector đã được chuẩn hoá điểm số:

- **Vector A (Câu query của người tìm kiếm: "Máy tính")**: $A = [1, 1, 0]$
- **Vector B (Bài báo 1: "Máy tính của Apple")**: $B = [1, 1, 1]$
- **Vector C (Bài báo 2: "Các mỏ than trên tính")** _(lưu ý chữ tính sai bối cảnh)_: $C = [0, 1, 0]$

Chúng ta sẽ đo xem bài báo nào (B hay C) giống với câu hỏi (A) hơn bằng **Cosine Similarity**.

### Xét Cặp A và B

**Bước 1: Tính tích vô hướng (Tử số)**
$$ \mathbf{A} \cdot \mathbf{B} = (1 \times 1) + (1 \times 1) + (0 \times 1) = 1 + 1 + 0 = \mathbf{2} $$

**Bước 2: Tính độ lớn của A và B (Mẫu số)**
$$ \|\mathbf{A}\| = \sqrt{1^2 + 1^2 + 0^2} = \sqrt{1 + 1} = \mathbf{\sqrt{2}} \approx 1.41 $$
$$ \|\mathbf{B}\| = \sqrt{1^2 + 1^2 + 1^2} = \sqrt{1 + 1 + 1} = \mathbf{\sqrt{3}} \approx 1.73 $$

**Bước 3: Gộp vào công thức Cosine**
$$ \text{Cosine}(A, B) = \frac{2}{\sqrt{2} \times \sqrt{3}} = \frac{2}{\sqrt{6}} \approx \mathbf{0.816} $$

### Xét Cặp A và C

**Bước 1: Tính tích vô hướng (Tử số)**
$$ \mathbf{A} \cdot \mathbf{C} = (1 \times 0) + (1 \times 1) + (0 \times 0) = 0 + 1 + 0 = \mathbf{1} $$

**Bước 2: Tính độ lớn của A và C (Mẫu số)**
$$ \|\mathbf{A}\| = \mathbf{\sqrt{2}} \approx 1.41 $$
$$ \|\mathbf{C}\| = \sqrt{0^2 + 1^2 + 0^2} = \sqrt{1} = \mathbf{1} $$

**Bước 3: Gộp vào công thức Cosine**
$$ \text{Cosine}(A, C) = \frac{1}{\sqrt{2} \times 1} \approx \mathbf{0.707} $$

**Kết luận Hệ thống Search:**

- Vì $0.816 > 0.707$ nên bài báo **B** được cho là liên quan và có nội dung tương đồng với câu truy vấn **A** hơn bài báo **C**.
- Hệ thống sẽ trả kết quả tìm kiếm xếp bài **B** lên top 1 và bài **C** xuống top 2.

---

## 4. Tại sao lại dùng Góc (Cosine) thay vì Khoảng Cách (Euclidean)?

Hãy tưởng tượng **Văn bản 1** chỉ là 1 câu: _"Bạn rất giỏi"_.
**Văn bản 2** là một đoạn văn lặp đi lặp lại câu đó 100 lần: _"Bạn rất giỏi. Bạn rất giỏi. ... (x100)"_.

Về mặt độ dài vector (tần suất đếm số chữ do TF-IDF quy định), Văn bản 2 sẽ rất "dài" hay "to lớn" (nằm xa hẳn ở một chỗ khác trong không gian hệ trục tọa độ). Nếu ta dùng thước để đo khoảng cách vật lý của chúng (Distance), kết quả sẽ ra lỗi là **Hai bài không giống nhau vì chúng nằm cách nhau quá xa**.

Tuy nhiên, về ngữ nghĩa, chúng đều biểu đạt một chủ đề: "Khen bạn học giỏi". Nếu ta kể một đường thẳng từ gốc tọa độ O lên hai điểm đó, hai đường thẳng sẽ **hoàn toàn đè lên nhau (góc chênh lệch bằng 0 độ)**. Cosine Similarity đo góc lệnh, từ đó nhận diện được ngay "À, đây cùng hướng (chung bản chất/ý định), chỉ là bài 2 nó đang Spam dài dòng hơn mà thôi".

Đó là lý do tại sao Cosine là tiêu chuẩn vàng của hệ thống Search (IR)!

---

## 5. Áp Dụng Thực Tiễn Trọng Hệ Thống (vnsearch-engine)

Trong dự án của bạn, việc tìm kiếm dựa trên chữ `TF-IDF` hay Vector hóa nhúng `Embedding` đều cần đo khoảng cách để lấy Top kết quả chuẩn.

Thay vì Code vòng lặp mảng của Python thủ công để tính Cosine (rất chậm), hệ thống của bạn (có lẽ là dựa trên vector database **Qdrant**) sẽ tối ưu hóa cấu trúc bộ nhớ.

Khi tạo chỉ mục (Collection) trên **Qdrant**, bạn thường cấu hình `distance=models.Distance.COSINE`. Qdrant sử dụng lõi tính toán song song xịn sò bằng ngôn ngữ Rust/C++ để bắn truy vấn và tính góc (Cosine) tự động cho hàng triệu văn bản chỉ trong vài chục mili-giây và đẩy trực tiếp kết quả ID về cho máy chủ Python `irs_api` phục vụ người dùng.
