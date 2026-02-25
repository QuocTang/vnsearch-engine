# Thuật Toán TF-IDF (Term Frequency - Inverse Document Frequency)

## 1. Giới Thiệu Chung

**TF-IDF** (viết tắt của Term Frequency – Inverse Document Frequency) là một trong những thuật toán kinh điển và quan trọng nhất trong lĩnh vực Xử lý Ngôn ngữ Tự nhiên (NLP) và Trích xuất Số liệu/Thông tin (Information Retrieval).

Thuật toán này thống kê và tính toán trọng số (weight) để đánh giá "tầm quan trọng" của một từ (term) đối với một văn bản (document) nằm trong một tập hợp văn bản (corpus/collection).

Cốt lõi của TF-IDF dựa trên hai luận điểm chính:

1. Nếu một từ xuất hiện nhiều lần trong một văn bản cụ thể thì từ đó có vẻ quan trọng và mang tính đại diện cho văn bản đó (**TF - Tần suất từ** cao).
2. Tuy nhiên, nếu từ đó lại xuất hiện rất phổ biến trong hầu hết tất cả các văn bản khác trong toàn bộ cơ sở dữ liệu (ví dụ: các từ "và", "hoặc", "là", "thì"), thì giá trị phân loại của nó gần như không có. Thuật toán cần trừng phạt (phân bổ trọng số thấp) cho các từ này (**IDF - Nghịch đảo tần suất văn bản**).

Kết hợp lại, một từ sẽ có điểm TF-IDF cao khi và chỉ khi: Nó **xuất hiện nhiều lần ở một bài viết cụ thể** (TF cao) nhưng lại **hiếm gặp ở các bài viết khác** (IDF cao).

---

## 2. Nền Tảng Toán Học

### 2.1. TF (Term Frequency) - Tần suất từ

`TF` tính toán tần số xuất hiện của một từ (gọi là $t$) trong một văn bản (gọi là $d$).

Công thức nguyên thủy đơn giản nhất:
$$ \text{TF}(t, d) = \frac{f*{t,d}}{\sum*{t' \in d} f\_{t',d}} $$

- $f_{t,d}$: Số lần từ $t$ xuất hiện trong văn bản $d$.
- $\sum_{t' \in d} f_{t',d}$: Tổng số tất cả các từ trong văn bản $d$.

_Trong các hệ thống thực tế (như Scikit-learn), TF được biến thể một chút để chống lại sự sai lệch của văn bản quá dài bằng cách dùng logarit của $f_{t,d}$._

### 2.2. IDF (Inverse Document Frequency) - Nghịch đảo tần suất văn bản

`IDF` đánh giá mức độ phổ biến phổ quát của từ $t$ trong toàn bộ tập văn bản $D$.

Công thức chuẩn:
$$ \text{IDF}(t, D) = \log \left( \frac{N}{|\{d \in D : t \in d\}|} \right) $$

- $N$: Tổng số lượng văn bản trong hệp / tập dữ liệu $D$.
- $|\{d \in D : t \in d\}|$: Số lượng văn bản có chứa từ $t$.
- _Lưu ý:_ Thực tế, người ta thường cộng 1 vào mẫu số: $\log\left(\frac{N}{1 + df}\right)$ để chống lỗi chia cho 0 nếu từ đó chưa từng xuất hiện.

### 2.3. Trọng số TF-IDF

Điểm TF-IDF của từ $t$ trong văn bản $d$ là tích số của TF và IDF:
$$ \text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D) $$

Càng lớn, từ khóa đó càng đặc trưng cho văn bản.

---

## 3. Ví Dụ Minh Hoạ Toàn Diện (Example)

Giả sử chúng ta có một cơ sở dữ liệu (Corpus) gồm 3 văn bản ngắn (câu):

- **Văn bản A (d1)**: "con mèo ăn con chuột"
- **Văn bản B (d2)**: "con chó đuổi con mèo"
- **Văn bản C (d3)**: "chuột ăn lúa"

**Bước 1: Tính toán TF (Term Frequency)**
Tách từ, ta có từ điển (vocabulary) bao gồm: `con, mèo, ăn, chuột, chó, đuổi, lúa`.

Ta tính TF đơn giản (bằng số đếm tự nhiên / tổng chữ):
_Với Văn bản A (Tổng = 5 chữ)_:

- TF("con", d1) = 2/5 = 0.4
- TF("mèo", d1) = 1/5 = 0.2
- TF("ăn", d1) = 1/5 = 0.2
- TF("chuột", d1) = 1/5 = 0.2
- TF("chó", d1) = 0/5 = 0
  _... (Tương tự cho d2 và d3)_

**Bước 2: Tính toán IDF (Inverse Document Frequency)**
Tổng số văn bản $N = 3$. Logarit ở đây chúng ta giả sử dùng log (cơ số 10) để dễ hình dung, chuẩn thì có thể là cơ số tự nhiên log(e).

- Chữ **"con"**: Xuất hiện trong 2 văn bản (d1, d2).
  -> IDF("con") = $log(\frac{3}{2}) = log(1.5) \approx 0.176$
- Chữ **"mèo"**: Xuất hiện trong 2 văn bản (d1, d2).
  -> IDF("mèo") = $log(\frac{3}{2}) = log(1.5) \approx 0.176$
- Chữ **"ăn"**: Xuất hiện trong 2 văn bản (d1, d3).
  -> IDF("ăn") = $log(\frac{3}{2}) = log(1.5) \approx 0.176$
- Chữ **"chuột"**: Xuất hiện trong 2 văn bản (d1, d3).
  -> IDF("chuột") = $log(\frac{3}{2}) = log(1.5) \approx 0.176$
- Chữ **"chó"**: Chỉ xuất hiện trong đúng 1 văn bản B (d2).
  -> IDF("chó") = $log(\frac{3}{1}) = log(3) \approx 0.477$ (Rất cao!)
- Chữ **"lúa"**: Chỉ xuất hiện trong đúng 1 văn bản C (d3).
  -> IDF("lúa") = $log(\frac{3}{1}) = log(3) \approx 0.477$ (Rất cao!)

**Bước 3: Tính toán TF-IDF** (Kết nạp D1)
Ví dụ đánh giá các từ với **Văn bản A (d1)**:

- $\text{TF-IDF}("con", d1)$ = $0.4 \times 0.176 \approx \mathbf{0.070}$
- $\text{TF-IDF}("mèo", d1)$ = $0.2 \times 0.176 \approx \mathbf{0.035}$
- $\text{TF-IDF}("chó", d1)$ = $0 \times 0.477 = \mathbf{0}$
- $\text{TF-IDF}("lúa", d1)$ = $0 \times 0.477 = \mathbf{0}$

_Nhận xét:_ Hệ thống thấy rõ từ "con" có điểm cao ở Document 1 do xuất hiện lặp lại nhiều lần. Những từ điển hình hiếm sẽ có điểm rất cao trong vector khi xuất hiện.

Cuối cùng, từng đoạn text sẽ chuyển hoá thành một "Vector 1 chiều" đại diện cho bài viết. Hệ thống máy sẽ dùng phép Đo khoảng cách Cosine (Cosine Similarity) để so sánh xem Vector tìm kiếm người dùng nạp vào có giống với Vector của các bài báo hay không.

---

## 4. Ứng Dụng Trong Hệ Thống (vnsearch-engine)

Trong source code của chúng ta (file `tfidf_service.py`), thư viện Scikit-learn (`TfidfVectorizer`) đã đóng gói sẵn các công thức trừu tượng bên trên cực kỳ tối ưu (dùng ma trận thừa – Sparse Matrix để chống hao tổn RAM).

Ta chỉ cần thiết lập các tham số khống chế giới hạn như:

- `max_features` (giới hạn kích thước từ vựng để tránh bùng nổ chiều không gian).
- `min_df` (loại bỏ lỗi chính tả xuất hiện ít trên tổng Database).
- `max_df` (loại bỏ từ phổ biến).
  Tiến hành `train` để tính ra cột `IDF` của toàn bộ dữ liệu, và gọi `transform` để xuất ra Vector TF-IDF điểm số cho bất kỷ chuỗi từ nào.
