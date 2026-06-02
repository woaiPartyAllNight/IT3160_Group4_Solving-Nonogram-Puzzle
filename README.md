# Nonogram Solver

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cài đặt và chạy chương trình](#cài-đặt-và-chạy-chương-trình)
- [Định dạng file đầu vào](#định-dạng-file-đầu-vào)
- [Kết quả đầu ra](#kết-quả-đầu-ra)
- [Thuật toán sử dụng](#thuật-toán-sử-dụng)
- [Thành viên nhóm](#thành-viên-nhóm)
- [Nguồn tham khảo](#nguồn-tham-khảo)

---

## Giới thiệu

**Nonogram** (còn gọi là Picross hoặc Paint by Numbers) là một thể loại trò chơi giải đố trên lưới ô vuông, trong đó người chơi cần tô đen các ô theo đúng gợi ý số cho trước ở mỗi hàng và mỗi cột. Mỗi con số trong gợi ý biểu thị độ dài của một đoạn ô liên tiếp được tô đen, và các đoạn này phải cách nhau ít nhất một ô trắng. Khi giải đúng, toàn bộ lưới sẽ tái tạo thành một hình ảnh nhị phân.

Tham khảo thêm: [Nonogram — Wikipedia](https://en.wikipedia.org/wiki/Nonogram)

**Mục tiêu của chương trình** là tự động giải các bài toán Nonogram với kích thước tùy ý (điển hình từ 5x5 đến 50x50) dựa trên bộ gợi ý hàng và cột được cung cấp dưới dạng file văn bản. Chương trình áp dụng kết hợp suy luận logic và tìm kiếm có quay lui để tìm ra toàn bộ nghiệm hợp lệ, đồng thời cung cấp giao diện trực quan hóa từng bước giải bằng thư viện Pygame.

---

## Cấu trúc thư mục

```
IT3160_Group4_Solving-Nonogram-Puzzle/
│
├── src/
│   ├── solver/                   # Phần nhân chính của chương trình
│   │   ├── main.py               # Điểm khởi chạy chương trình solver
│   │   ├── nonogram_solver.py    # Lớp NonogramSolver — giao diện chính
│   │   ├── backtrack.py          # Thuật toán backtracking + heuristic MRV
│   │   ├── logical.py            # Điều phối toàn bộ các quy tắc suy luận
│   │   ├── base.py               # Khởi tạo bảng và cấu trúc bound
│   │   ├── config.py             # Đường dẫn file input mặc định
│   │   ├── utils.py              # Tiện ích: đọc file, kiểm tra nghiệm, Visualizer
│   │   ├── input.txt             # File đầu vào mẫu
│   │   └── rules/                # Các quy tắc suy luận
│   │       ├── overlap_inference.py    # Quy tắc 1: tô ô giao nhau
│   │       ├── bound_tightening.py     # Quy tắc 2: siết chặt giới hạn khối
│   │       ├── anchor_propagation.py   # Quy tắc 3: lan truyền từ ô cố định
│   │       └── segment_utils.py        # Tiện ích xử lý đoạn
│   │
│
│── benchmark.py                  # Tool chạy code để kiểm thử thời gian
└── README.md
```

> Lưu ý: Một số file test nặng chưa được đưa lên repository. Phần `src/api_picture/` và `src/util/` là hướng phát triển tương lai (nhận dạng ảnh), không ảnh hưởng đến chức năng solver hiện tại.

---

## Cài đặt và chạy chương trình

### Yêu cầu

- **Python 3.8** trở lên
- **pip** (trình quản lý gói Python)
- Terminal hoặc IDE tùy chọn (VS Code, PyCharm, v.v.)

Đây là dự án Python thuần, không yêu cầu bước biên dịch như các ngôn ngữ C/C++.

### Clone repository

```bash
git clone https://github.com/<tên-tài-khoản>/IT3160_Group4_Solving-Nonogram-Puzzle.git
cd IT3160_Group4_Solving-Nonogram-Puzzle
```

### Cài đặt thư viện phụ thuộc

Cài đặt các thư viện được sử dụng trong mã nguồn:

```bash
pip install pygame
```

> Nếu có thêm thư viện khác, hãy cài đặt theo các câu lệnh `import` trong mã nguồn tương ứng.

### Chuẩn bị file đầu vào

Chỉnh sửa file `src/solver/input.txt` theo định dạng mô tả ở mục dưới, hoặc sử dụng file mẫu sẵn có trong repository.

### Chạy chương trình

```bash
cd src
python solver/main.py
```

Mặc định chương trình đọc file `src/solver/input.txt`. Để thay đổi đường dẫn, chỉnh sửa biến `INPUT_FILE` trong `src/solver/config.py`.

---

## Định dạng file đầu vào

File `input.txt` có cấu trúc như sau:

```
m n
<gợi ý hàng 1>
<gợi ý hàng 2>
...
<gợi ý hàng m>
<gợi ý cột 1>
<gợi ý cột 2>
...
<gợi ý cột n>
```

Trong đó:

- Dòng đầu tiên gồm hai số nguyên `m` và `n`, lần lượt là số hàng và số cột của lưới.
- `m` dòng tiếp theo, mỗi dòng là danh sách các số nguyên dương cách nhau bởi dấu cách, biểu thị độ dài các đoạn tô đen liên tiếp trên hàng tương ứng (đọc từ trái sang phải).
- `n` dòng tiếp theo, mỗi dòng tương tự nhưng cho cột (đọc từ trên xuống dưới).
- Hàng hoặc cột hoàn toàn trắng được biểu thị bằng `0`.

**Ví dụ — lưới 5x5:**

```
5 5
1
3
3
3
1 1 1
2 2
1 1
4
1
1 1
```

Giải thích: lưới 5 hàng, 5 cột. Hàng 1 có 1 ô đen, hàng 2 có 3 ô đen liên tiếp, hàng 5 có 3 đoạn mỗi đoạn 1 ô. Tương tự cho các cột.

**Ví dụ — lưới 20x20** (xem file `src/solver/input.txt` trong repository để tham khảo bài toán kích thước lớn hơn).

---

## Kết quả đầu ra

### In ra terminal

Sau khi tìm được nghiệm, chương trình in kết quả trực tiếp ra terminal theo định dạng ký tự:

- `#` — ô được tô đen
- `.` — ô xác định là trắng
- ` ` (khoảng trắng) — ô chưa xác định (trường hợp không tìm đủ nghiệm)

Ví dụ kết quả một nonogram 5x5:

```
..#..
.###.
#####
.###.
..#..
```

Chương trình cũng thông báo số lượng nghiệm tìm được:

```
[+] Thành công! Tìm thấy 1 nghiệm.
[+] Kết quả nghiệm đầu tiên:
```

### Trực quan hóa từng bước (Visualizer)

Khi biến `use_visualize = True` trong `main.py`, chương trình mở một cửa sổ đồ họa Pygame hiển thị quá trình giải theo từng bước. Giao diện bao gồm:

- Lưới ô màu với ba trạng thái: ô đen, ô trắng (dấu X), ô chưa xác định.
- Gợi ý hàng và cột hiển thị bên trái và phía trên lưới.
- Thanh trượt (slider) để duyệt qua các bước giải đã ghi lại.
- Nút Play/Pause để phát lại tự động quá trình giải.
- Hỗ trợ điều hướng bằng phím mũi tên trái/phải.

Để tắt visualizer (chạy nhanh hơn), đặt `use_visualize = False` trong `src/solver/main.py`.

---

## Thuật toán sử dụng

Chương trình áp dụng chiến lược kết hợp giữa suy luận logic và tìm kiếm có quay lui, tổ chức theo hai lớp chính:

### 1. Suy luận logic (Logical Inference)

Trước khi thử từng khả năng, chương trình cố gắng suy ra giá trị các ô bằng các quy tắc logic. Ba nhóm quy tắc được áp dụng lặp đi lặp lại cho đến khi không còn thay đổi:

**Quy tắc 1 — Giao nhau (Overlap Inference):** Nếu vị trí sớm nhất và muộn nhất mà một khối có thể đặt có phần giao nhau, các ô trong vùng giao đó chắc chắn được tô đen.

**Quy tắc 2 — Siết chặt giới hạn (Bound Tightening):** Căn cứ vào vị trí các khối khác và các ô đã biết, thu hẹp phạm vi khả dĩ của từng khối. Ví dụ: nếu ô ngay trước giới hạn bắt đầu đã được tô đen, giới hạn bắt đầu phải được đẩy sang phải.

**Quy tắc 3 — Lan truyền từ ô cố định (Anchor Propagation):** Khi một ô đầu/cuối của phạm vi đã được tô đen, suy ra toàn bộ đoạn tô và đánh dấu ô ngăn cách sau/trước đoạn đó.

### 2. Backtracking kết hợp MRV

Khi suy luận không còn tiến triển được mà bảng chưa hoàn chỉnh, chương trình chuyển sang tìm kiếm có quay lui:

**MRV (Minimum Remaining Values):** Thay vì thử ô theo thứ tự cố định, chương trình chọn ô chưa xác định thuộc hàng và cột có ít ô trống nhất — tức ô bị ràng buộc nhiều nhất. Chiến lược này giúp phát hiện mâu thuẫn sớm hơn, giảm đáng kể không gian tìm kiếm.

**Backtracking:** Với ô được chọn, chương trình thử lần lượt hai giá trị (trắng hoặc đen). Sau mỗi lần gán, toàn bộ quy trình suy luận logic được chạy lại. Nếu phát hiện mâu thuẫn, chương trình quay lui và thử giá trị còn lại.

Cách tiếp cận này đảm bảo tìm được toàn bộ nghiệm hợp lệ và hoạt động hiệu quả với các bảng kích thước trung bình đến lớn.

---

## Thành viên nhóm

- Nguyễn Xuân Thành
- Chu Văn Hào
- Nguyễn Việt Anh
- Nguyễn Tuấn Bằng

---

## Nguồn tham khảo

[1] Chiung-Hsueh Yu, Hui-Lung Lee, Ling-Hwei Chen, “An efficient algorithm for solving
nonograms”, Applied Intelligence, Springer, 2011.
[2] Nobuhisa Ueda, Tadaaki Nagao, “NP-completeness results for NONOGRAM via
parsimonious reductions”, Technical Report TR96-0008, Tokyo Institute of Technology,
1996.
[3] K. J. Batenburg, W. A. Kosters, “Solving Nonograms by combining relaxations”, Pattern
Recognition, 2009.
[4] Stuart Russell, Peter Norvig, Artificial Intelligence: A Modern Approach, Pearson.
[5] Wikipedia contributors, “Nonogram”, Wikipedia, The Free Encyclopedia.
