# KỊCH BẢN TEST VÀ DEMO

## PHẦN 1: TEST DEADLOCK SIMULATION

### Kịch bản 1: Deadlock đơn giản (2 processes, 2 resources)

**Cấu hình:**
- Số tiến trình: 2 (P0, P1)
- Số tài nguyên: 2 (R0, R1)

**Các bước thực hiện:**

1. **Bước 1:** Allocate R0 cho P0
   - Chọn P0, chọn R0
   - Nhấn "Allocate"
   - ✅ Kết quả: P0 giữ R0, trạng thái "Running"

2. **Bước 2:** Allocate R1 cho P1
   - Chọn P1, chọn R1
   - Nhấn "Allocate"
   - ✅ Kết quả: P1 giữ R1, trạng thái "Running"

3. **Bước 3:** P0 yêu cầu R1
   - Chọn P0, chọn R1
   - Nhấn "Request"
   - ⚠️ Kết quả: P0 bị "Blocked" (R1 đang được P1 giữ)
   - Graph: P0 -> R1 (đường đứt màu cam)

4. **Bước 4:** P1 yêu cầu R0
   - Chọn P1, chọn R0
   - Nhấn "Request"
   - 🔴 Kết quả: DEADLOCK DETECTED!
   - Graph: Chu trình P0 -> R1 -> P1 -> R0 -> P0 (màu đỏ)
   - Dialog: "WARNING: PROCESS DEADLOCK IS DETECTED!"

**Kết quả mong đợi:**
- Cả P0 và P1 đều chuyển sang màu đỏ
- R0 và R1 cũng chuyển sang màu đỏ
- Log hiển thị chu trình deadlock

---

### Kịch bản 2: Deadlock phức tạp (3 processes, 3 resources)

**Cấu hình:**
- Số tiến trình: 3 (P0, P1, P2)
- Số tài nguyên: 3 (R0, R1, R2)

**Các bước:**

1. P0 allocate R0
2. P1 allocate R1
3. P2 allocate R2
4. P0 request R1 (blocked)
5. P1 request R2 (blocked)
6. P2 request R0 (DEADLOCK!)
   - Chu trình: P0 -> P1 -> P2 -> P0

---

### Kịch bản 3: Không có Deadlock (giải phóng tài nguyên)

**Các bước:**

1. P0 allocate R0
2. P1 allocate R1
3. P0 request R1 (blocked)
4. **P1 release R1** ← Điểm khác biệt
   - ✅ R1 được cấp cho P0 ngay lập tức
   - P0 không bị blocked nữa
5. Nhấn "Phát hiện Deadlock"
   - ✅ Kết quả: "Không có deadlock"

---

### Kịch bản 4: Test reset

**Các bước:**

1. Tạo deadlock theo kịch bản 1
2. Nhấn "Reset"
3. ✅ Kiểm tra:
   - Tất cả edges bị xóa
   - Tất cả processes về trạng thái "Ready"
   - Tất cả resources về trạng thái "Free"
   - Graph được vẽ lại sạch sẽ

---

## PHẦN 2: TEST BANKER'S ALGORITHM

### Kịch bản 1: Kiểm tra trạng thái an toàn (Dữ liệu mẫu)

**Dữ liệu:**
```
n = 5, m = 3
Available = [3, 3, 2]

Max:
P0: [7, 5, 3]
P1: [3, 2, 2]
P2: [9, 0, 2]
P3: [2, 2, 2]
P4: [4, 3, 3]

Allocation:
P0: [0, 1, 0]
P1: [2, 0, 0]
P2: [3, 0, 2]
P3: [2, 1, 1]
P4: [0, 0, 2]

Need (tự động):
P0: [7, 4, 3]
P1: [1, 2, 2]
P2: [6, 0, 0]
P3: [0, 1, 1]
P4: [4, 3, 1]
```

**Các bước:**

1. Nhấn "Dữ liệu mẫu"
2. Nhấn "Kiểm tra trạng thái an toàn"
3. ✅ Kết quả mong đợi:
   ```
   Bước 1: P1 chạy được (Need[1] = [1,2,2] <= Work = [3,3,2])
           Work = [5, 3, 2]
   
   Bước 2: P3 chạy được (Need[3] = [0,1,1] <= Work = [5,3,2])
           Work = [7, 4, 3]
   
   Bước 3: P4 chạy được (Need[4] = [4,3,1] <= Work = [7,4,3])
           Work = [7, 4, 5]
   
   Bước 4: P0 chạy được (Need[0] = [7,4,3] <= Work = [7,4,5])
           Work = [7, 5, 5]
   
   Bước 5: P2 chạy được (Need[2] = [6,0,0] <= Work = [7,5,5])
           Work = [10, 5, 7]
   
   => AN TOÀN
   Chuỗi an toàn: P1 -> P3 -> P4 -> P0 -> P2
   ```

---

### Kịch bản 2: Yêu cầu tài nguyên - CHẤP NHẬN

**Tiền đề:** Dữ liệu mẫu đã load

**Yêu cầu:**
- Tiến trình: P1
- Request: [1, 0, 2]

**Các bước:**

1. Nhấn "Yêu cầu tài nguyên"
2. Chọn P1
3. Nhập [1, 0, 2]
4. Nhấn "Gửi yêu cầu"

**Kết quả mong đợi:**

```
=== XỬ LÝ YÊU CẦU TÀI NGUYÊN ===
Tiến trình: P1
Request[1] = [1, 0, 2]

Bước 1: Kiểm tra Request[i] <= Need[i]
  ✓ Request = [1, 0, 2] <= Need[1] = [1, 2, 2]

Bước 2: Kiểm tra Request[i] <= Available
  ✓ Request = [1, 0, 2] <= Available = [3, 3, 2]

Bước 3: Giả lập cấp phát tài nguyên
  Available_mới = [2, 3, 0]
  Allocation[1]_mới = [3, 0, 2]
  Need[1]_mới = [0, 2, 0]

Bước 4: Chạy Safety Algorithm với trạng thái mới
  Work = [2, 3, 0]
  Bước 1: P1 chạy được...
  Bước 2: P3 chạy được...
  ...
  => Trạng thái AN TOÀN
  Chuỗi an toàn: P1 -> P3 -> P4 -> P2 -> P0

KẾT QUẢ: YÊU CẦU ĐƯỢC CHẤP NHẬN
✅ P1 được cấp phát [1, 0, 2]
```

**Kiểm tra:** Ma trận trên GUI đã được cập nhật

---

### Kịch bản 3: Yêu cầu tài nguyên - TỪ CHỐI (Unsafe)

**Yêu cầu:**
- Tiến trình: P0
- Request: [0, 2, 0]

**Các bước:**

1. Nhấn "Yêu cầu tài nguyên"
2. Chọn P0
3. Nhập [0, 2, 0]
4. Nhấn "Gửi yêu cầu"

**Kết quả mong đợi:**

```
=== XỬ LÝ YÊU CẦU TÀI NGUYÊN ===
Tiến trình: P0
Request[0] = [0, 2, 0]

Bước 1: ✓ Request <= Need
Bước 2: ✓ Request <= Available

Bước 3: Giả lập
  Available_mới = [3, 1, 2]
  Allocation[0]_mới = [0, 3, 0]

Bước 4: Safety Check
  Work = [3, 1, 2]
  Không tìm thấy tiến trình nào chạy được!
  => KHÔNG AN TOÀN

KẾT QUẢ: YÊU CẦU BỊ TỪ CHỐI
❌ Trạng thái mới không an toàn
P0 phải chờ
Rollback về trạng thái cũ
```

**Kiểm tra:** Ma trận KHÔNG thay đổi (rollback thành công)

---

### Kịch bản 4: Lỗi - Request > Need

**Yêu cầu:**
- Tiến trình: P1
- Request: [2, 3, 3] (lớn hơn Need[1] = [1, 2, 2])

**Kết quả mong đợi:**

```
Bước 1: Kiểm tra Request[i] <= Need[i]
  LỖI: Request = [2, 3, 3] > Need[1] = [1, 2, 2]
  Tiến trình yêu cầu vượt quá nhu cầu tối đa!

Dialog: "Request vượt quá Need!
         Tiến trình yêu cầu nhiều hơn nhu cầu tối đa đã khai báo."
```

---

### Kịch bản 5: Lỗi - Request > Available

**Yêu cầu:**
- Tiến trình: P2
- Request: [5, 0, 0] (Available = [3, 3, 2])

**Kết quả mong đợi:**

```
Bước 1: ✓ Request <= Need
Bước 2: Kiểm tra Request[i] <= Available
  LỖI: Request = [5, 0, 0] > Available = [3, 3, 2]
  P2 phải chờ (tài nguyên không đủ)!

Dialog: "Không đủ tài nguyên
         Request = [5, 0, 0]
         Available = [3, 3, 2]
         P2 phải chờ!"
```

---

### Kịch bản 6: Trạng thái không an toàn từ đầu

**Dữ liệu:**
```
n = 3, m = 3
Available = [1, 0, 0]

Max:
P0: [5, 5, 5]
P1: [4, 4, 4]
P2: [3, 3, 3]

Allocation:
P0: [3, 2, 2]
P1: [2, 2, 2]
P2: [1, 1, 1]

Need:
P0: [2, 3, 3]
P1: [2, 2, 2]
P2: [2, 2, 2]
```

**Các bước:**

1. Nhập dữ liệu trên
2. Nhấn "Cập nhật dữ liệu"
3. Nhấn "Kiểm tra trạng thái an toàn"

**Kết quả mong đợi:**

```
Work = [1, 0, 0]

Không tìm thấy tiến trình nào có thể chạy!
(Tất cả Need > Work)

=== KẾT QUẢ: KHÔNG AN TOÀN ===
Hệ thống có thể rơi vào deadlock.

Dialog: "Trạng thái KHÔNG AN TOÀN!
         Hệ thống có thể rơi vào deadlock."
```

---

### Kịch bản 7: Cấu hình tùy chỉnh

**Các bước:**

1. Nhập n = 4, m = 2
2. Nhấn "Khởi tạo ma trận"
3. Chỉnh sửa:
   ```
   Available = [3, 2]
   
   Max:
   P0: [5, 2]
   P1: [4, 3]
   P2: [3, 2]
   P3: [2, 1]
   
   Allocation:
   P0: [2, 0]
   P1: [1, 1]
   P2: [1, 1]
   P3: [0, 0]
   ```
4. Nhấn "Cập nhật dữ liệu"
5. Kiểm tra Need tự động tính
6. Chạy Safety Check

**Kết quả mong đợi:**
- Need được tính đúng:
  ```
  P0: [3, 2]
  P1: [3, 2]
  P2: [2, 1]
  P3: [2, 1]
  ```
- Safety check chạy thành công

---

## PHẦN 3: EDGE CASES & ERROR HANDLING

### Test 1: Cấu hình số âm
- Nhập n = -1
- ✅ Error: "Số lượng phải lớn hơn 0"

### Test 2: Cấu hình quá lớn
- Nhập n = 100, m = 100
- ✅ Chương trình xử lý được nhưng chậm

### Test 3: Parse lỗi dữ liệu
- Nhập Available = "[3, 3, abc]"
- ✅ Error: "Không thể parse dữ liệu"

### Test 4: Request với format sai
- Nhập Request = "1, 0, 2" (thiếu [])
- ✅ Error: "Dữ liệu không hợp lệ"

### Test 5: Allocate tài nguyên đang được giữ
- P0 đang giữ R0
- Allocate R0 cho P1
- ✅ Warning: "Tài nguyên R0 đang được giữ bởi P0!"

### Test 6: Release tài nguyên không giữ
- P0 không giữ R1
- Release R1 từ P0
- ✅ Warning: "P0 không đang giữ R1!"
