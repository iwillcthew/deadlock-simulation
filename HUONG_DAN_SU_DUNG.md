# HƯỚNG DẪN SỬ DỤNG
## Công cụ Mô phỏng Deadlock & Banker's Algorithm

### I. CÁCH CHẠY CHƯƠNG TRÌNH
   ```bash
   python main.py
   ```

### II. TAB 1: MÔ PHỎNG DEADLOCK

#### Mục đích:
- Mô phỏng tự động các kịch bản deadlock
- Trực quan hóa Resource Allocation Graph
- Phát hiện deadlock tự động

#### Các bước sử dụng:

**1. Nhập kịch bản:**

**Định dạng lệnh:**
```
<action> <process> <resource>
```

Trong đó:
- `action`: `allocate`, `request`, hoặc `release`
- `process`: Tên tiến trình (P0, P1, P2, ...)
- `resource`: Tên tài nguyên (R0, R1, R2, ...)

**Ví dụ kịch bản:**
```
allocate P0 R0
allocate P1 R1
request P0 R1
request P1 R0
```

**Chú thích:**
- Dòng bắt đầu bằng `#` là comment
- Dòng trống sẽ bị bỏ qua

**2. Sử dụng dữ liệu mẫu:**

Có 2 mẫu kịch bản có sẵn:

**a) Mẫu: Deadlock (4 tiến trình)**
- 4 tiến trình (P0, P1, P2, P3)
- 4 tài nguyên (R0, R1, R2, R3)
- 8 bước thực hiện
- Mỗi tiến trình cấp phát 1 tài nguyên, sau đó yêu cầu tài nguyên kế tiếp
- Tạo chu trình deadlock: P0 → P1 → P2 → P3 → P0
- Tất cả 4 tiến trình đều bị khóa

**b) Mẫu: Không Deadlock (5 tiến trình)**
- 5 tiến trình (P0, P1, P2, P3, P4)
- 4 tài nguyên (R0, R1, R2, R3)
- 16 bước thực hiện
- Minh họa quản lý tài nguyên hiệu quả
- Các tiến trình giải phóng đúng thời điểm
- Tất cả tiến trình hoàn thành thành công

**Cách dùng:**
1. Nhấn một trong 2 nút "Mẫu: ..."
2. Kịch bản sẽ được điền tự động vào textbox
3. Nhấn "Tải kịch bản"

**3. Chạy mô phỏng:**

**Tự động:**
1. Điều chỉnh tốc độ (100-3000ms)
2. Nhấn "▶ Bắt đầu"
3. Mô phỏng chạy tự động từng bước
4. Nhấn "⏸ Tạm dừng" để dừng tạm thời
5. Tiếp tục bằng "▶ Bắt đầu"

**Từng bước:**
1. Nhấn "→ Bước tiếp"
2. Mỗi lần nhấn thực hiện 1 bước
3. Xem kết quả từng bước chi tiết

**4. Kết quả mô phỏng:**

**Nếu có Deadlock:**
- Mô phỏng tự động dừng
- Dialog cảnh báo "DEADLOCK DETECTED!"
- Graph tô đỏ các tiến trình và tài nguyên trong deadlock
- Log hiển thị chu trình deadlock

**Nếu không có Deadlock:**
- Mô phỏng chạy hết kịch bản
- Thông báo "Kịch bản chạy xong! Không có Deadlock"
- Graph hiển thị trạng thái cuối cùng

**5. Ví dụ thực tế:**

**Tình huống 1: Tạo Deadlock đơn giản**
```
# Nhấn "Mẫu: Deadlock"
# Nhấn "Tải kịch bản"
# Nhấn "▶ Bắt đầu"

Bước 1: ALLOCATE P0 R0
  ✓ Cấp phát R0 cho P0

Bước 2: ALLOCATE P1 R1
  ✓ Cấp phát R1 cho P1

Bước 3: REQUEST P0 R1
  ⚠ P0 yêu cầu R1 - Bị chặn (R1 đang được giữ bởi P1)

Bước 4: REQUEST P1 R0
  ⚠ P1 yêu cầu R0 - Bị chặn (R0 đang được giữ bởi P0)
  🔴 DEADLOCK PHÁT HIỆN tại bước 4!

=> Dialog: "DEADLOCK DETECTED!"
=> Graph: P0 và P1 tô đỏ, chu trình rõ ràng
```

**Tình huống 2: Không có Deadlock**
```
# Nhấn "Mẫu: Không Deadlock"
# Nhấn "Tải kịch bản"
# Nhấn "→ Bước tiếp" nhiều lần

Bước 1: ALLOCATE P0 R0
Bước 2: ALLOCATE P1 R1
Bước 3: REQUEST P0 R1 (bị chặn)
Bước 4: RELEASE P1 R1
  ✓ P1 giải phóng R1 - Cấp phát cho P0
  (P0 không còn bị chặn)
Bước 5: RELEASE P0 R0
Bước 6: RELEASE P0 R1

=> Thông báo: "Kịch bản chạy xong! Không có Deadlock"
```

**6. Viết kịch bản tùy chỉnh:**

**Ví dụ: Deadlock với 3 tiến trình**
```
# Kịch bản tùy chỉnh
allocate P0 R0
allocate P1 R1
allocate P2 R2
request P0 R1
request P1 R2
request P2 R0
# Deadlock: P0->R1->P1->R2->P2->R0->P0
```

**Lưu ý khi viết:**
- Mỗi dòng là một lệnh
- Phải có đủ 3 phần: action process resource
- Processes và resources sẽ tự động tạo nếu chưa tồn tại
- Sử dụng # để comment

**7. Chú thích trên Graph:**
- **Hình tròn xanh**: Tiến trình Ready/Running
- **Hình tròn đỏ**: Tiến trình trong deadlock
- **Hình vuông vàng**: Tài nguyên rảnh
- **Hình vuông đỏ**: Tài nguyên trong deadlock
- **Mũi tên xanh liền**: Allocation (R → P)
- **Mũi tên cam đứt**: Request (P → R)
- **Mũi tên đỏ**: Edge trong deadlock

**8. Reset:**
- Nhấn "↻ Reset" để xóa toàn bộ
- Kịch bản cũ sẽ bị xóa, trở về trạng thái ban đầu

### III. TAB 2: BANKER'S ALGORITHM

#### Mục đích:
- Kiểm tra trạng thái an toàn của hệ thống
- Xử lý yêu cầu tài nguyên một cách an toàn
- Tránh deadlock

#### Các bước sử dụng:

**1. Khởi tạo dữ liệu:**

**Cách 1: Sử dụng dữ liệu mẫu**
- Nhấn "Dữ liệu mẫu"
- Hệ thống load sẵn:
  - 5 tiến trình (P0-P4)
  - 3 loại tài nguyên
  - Các ma trận Max, Allocation đã được điền sẵn

**Cách 2: Nhập thủ công**
- Nhập n = số tiến trình, m = số tài nguyên
- Nhấn "Khởi tạo ma trận"
- Chỉnh sửa trực tiếp trong các textbox:
  - **Available**: Vector tài nguyên có sẵn, ví dụ: `[3, 3, 2]`
  - **Max Matrix**: Nhu cầu tối đa của mỗi tiến trình
    ```
    P0: [7, 5, 3]
    P1: [3, 2, 2]
    P2: [9, 0, 2]
    ...
    ```
  - **Allocation Matrix**: Tài nguyên đã cấp phát
    ```
    P0: [0, 1, 0]
    P1: [2, 0, 0]
    ...
    ```
- Nhấn "Cập nhật dữ liệu"
- **Need Matrix** sẽ tự động tính: Need = Max - Allocation

**2. Kiểm tra trạng thái an toàn:**
- Nhấn "Kiểm tra trạng thái an toàn"
- Hệ thống chạy Safety Algorithm
- Kết quả:
  - **An toàn**: Hiển thị chuỗi an toàn (ví dụ: P1 -> P3 -> P4 -> P0 -> P2)
  - **Không an toàn**: Cảnh báo có nguy cơ deadlock

**3. Yêu cầu tài nguyên:**
- Nhấn "Yêu cầu tài nguyên"
- Dialog hiện ra:
  - Chọn tiến trình (ví dụ: P1)
  - Nhập vector Request (ví dụ: `[1, 0, 2]`)
  - Nhấn "Gửi yêu cầu"
- Hệ thống chạy Banker's Request Algorithm:
  1. Kiểm tra Request <= Need
  2. Kiểm tra Request <= Available
  3. Giả lập cấp phát
  4. Chạy Safety Algorithm với trạng thái mới
  5. **Nếu an toàn**: Chấp nhận yêu cầu, cập nhật ma trận
  6. **Nếu không an toàn**: Từ chối, rollback, P_i phải chờ

### IV. LƯU Ý QUAN TRỌNG

1. **Tab Deadlock:**
   - Kịch bản phải được tải trước khi chạy
   - Hệ thống tự động phát hiện deadlock khi có request bị chặn
   - Mô phỏng dừng ngay khi phát hiện deadlock
   - Sử dụng Reset để bắt đầu lại

2. **Tab Banker:**
   - Luôn cập nhật dữ liệu sau khi chỉnh sửa
   - Need Matrix tự động tính, không cần nhập
   - Request Algorithm đảm bảo hệ thống luôn ở trạng thái an toàn

### V. XỬ LÝ LỖI THƯỜNG GẶP

**Lỗi 1: "Vui lòng tải kịch bản trước!"**
- Nhấn "Tải kịch bản" trước khi chạy
- Đảm bảo kịch bản không rỗng

**Lỗi 2: "Định dạng không đúng"**
- Kiểm tra mỗi dòng có đủ 3 phần
- Ví dụ đúng: `allocate P0 R0`
- Ví dụ sai: `allocate P0` (thiếu resource)

**Lỗi 3: "Action không hợp lệ"**
- Chỉ chấp nhận: allocate, request, release
- Viết thường (lowercase)
