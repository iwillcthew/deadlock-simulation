# Bài tập lớn Hệ điều hành: Mô phỏng Deadlock & Giải thuật Banker

Dự án này là công cụ mô phỏng bằng Python và Tkinter để trực quan hóa hai khái niệm cốt lõi trong quản lý tài nguyên của hệ điều hành:

1. **Mô phỏng Deadlock (Deadlock Simulation):** Cho phép người dùng tạo ra một tình huống deadlock bằng cách cấp phát và yêu cầu tài nguyên thủ công.
    
2. **Tránh Deadlock (Deadlock Avoidance):** Hiện thực giải thuật Banker để đảm bảo hệ thống luôn ở trạng thái an toàn.
    

## Công nghệ sử dụng

- **Ngôn ngữ:** Python 3
    
- **Thư viện GUI:** Tkinter (có sẵn trong Python)
    

## Tính năng chính

### 1. Tab Mô phỏng Deadlock

Giao diện này cho phép người dùng nhập kịch bản và mô phỏng tự động để trực quan hóa deadlock.

- **Nhập kịch bản:** Người dùng nhập danh sách các thao tác theo định dạng:
    - `allocate <process> <resource>` - Cấp phát tài nguyên
    - `request <process> <resource>` - Yêu cầu tài nguyên
    - `release <process> <resource>` - Giải phóng tài nguyên
    - Ví dụ: `allocate P0 R0`, `request P1 R1`

- **Dữ liệu mẫu có sẵn:**
    - **Mẫu Deadlock:** Kịch bản với 4 tiến trình, tạo chu trình deadlock P0→P1→P2→P3→P0
    - **Mẫu Không Deadlock:** Kịch bản 5 tiến trình, 16 bước, giải phóng tài nguyên đúng lúc

- **Mô phỏng tự động:**
    - **Bắt đầu:** Chạy tự động từng bước với tốc độ tùy chỉnh
    - **Tạm dừng:** Dừng mô phỏng tạm thời
    - **Bước tiếp:** Thực hiện từng bước một
    - Điều chỉnh tốc độ mô phỏng (100-3000ms)

- **Phát hiện Deadlock tự động:**
    - Mỗi khi một yêu cầu bị chặn (blocked), hệ thống tự động chạy thuật toán phát hiện chu trình
    - **Trực quan hóa Deadlock:** Khi phát hiện chu trình, hệ thống hiển thị cảnh báo "WARNING: PROCESS DEADLOCK IS DETECTED" và tô đỏ các tiến trình, tài nguyên liên quan
    - Mô phỏng tự động dừng khi phát hiện deadlock
        

### 2. Tab Giải thuật Banker (Banker's Algorithm)

Giao diện này mô phỏng thuật toán Banker để tránh deadlock.

- **Thiết lập ban đầu:**
    
    - Nhập số lượng tiến trình (n).
        
    - Nhập số lượng loại tài nguyên (m).
        
    - Nhập vector `Available` (số lượng thực thể có sẵn của mỗi loại tài nguyên).
        
    - Nhập ma trận `Max` (nhu cầu tối đa của mỗi tiến trình).
        
    - Nhập ma trận `Allocation` (số tài nguyên đang được cấp phát cho mỗi tiến trình).
        
- **Tính toán tự động:**
    
    - Hệ thống tự động tính toán và hiển thị ma trận `Need` (`Need = Max - Allocation`).
        
- **Chức năng "Kiểm tra trạng thái an toàn" (Safety Check):**
    
    - Người dùng nhấn nút để chạy Thuật toán An toàn (Safety Algorithm).
        
    - Hộp thoại output sẽ hiển thị từng bước chạy của thuật toán:
        
        - `Work = Available`, `Finish = [F, F, ..., F]`
            
        - `Tìm thấy P_i thỏa mãn Need[i] <= Work...`
            
        - `P_i chạy xong. Work = Work + Allocation[i]. Finish[i] = T.`
            
        - ...
            
    - **Kết quả:** Hiển thị "Trạng thái an toàn. Chuỗi an toàn là: <P1, P3, ...>" hoặc "Trạng thái không an toàn!".
        
- **Chức năng "Yêu cầu tài nguyên" (Resource Request):**
    
    - Người dùng chọn tiến trình `P_i` và nhập vector `Request_i` (số tài nguyên `P_i` muốn yêu cầu).
        
    - Hệ thống chạy Thuật toán Yêu cầu (Banker's Request Algorithm):
        
        1. Kiểm tra `Request_i <= Need[i]`. (Nếu không, báo lỗi).
            
        2. Kiểm tra `Request_i <= Available`. (Nếu không, P_i phải chờ).
            
        3. **Giả lập cấp phát:**
            
            - `Available = Available - Request_i`
                
            - `Allocation[i] = Allocation[i] + Request_i`
                
            - `Need[i] = Need[i] - Request_i`
                
        4. Gọi Thuật toán An toàn (Safety Algorithm) với trạng thái _mới_ này.
            
        5. **Quyết định:**
            
            - Nếu trạng thái mới **an toàn**, chấp nhận yêu cầu. Cập nhật các ma trận trên GUI.
                
            - Nếu trạng thái mới **không an toàn**, từ chối yêu cầu. Hoàn trả lại trạng thái (rollback) và P_i phải chờ.
                
    - Toàn bộ quá trình này được ghi chi tiết ra hộp thoại output.
        

## Cấu trúc file 

```
+-- main.py             # File chạy chính, tạo cửa sổ Tkinter và các Tab
+-- deadlock_tab.py     # Class và logic cho Tab Mô phỏng Deadlock
+-- banker_tab.py       # Class và logic cho Tab Giải thuật Banker
+-- README.md           # File này
```

## Cách chạy
```bash
python main.py
```

**Yêu cầu hệ thống:**
- Python 3.6 trở lên
- Tkinter (có sẵn trong Python)
- Hệ điều hành: Windows/Linux/macOS


## Tài liệu đi kèm

📚 **Các file tài liệu quan trọng:**

1. **HUONG_DAN_SU_DUNG.md** - Hướng dẫn chi tiết cách sử dụng
2. **TEST_SCENARIOS.md** - Kịch bản test và demo


## Tính năng nổi bật

✨ **Tab Deadlock:**
- Trực quan hóa Resource Allocation Graph
- Các thao tác: Allocate, Request, Release
- Phát hiện deadlock tự động (DFS cycle detection)
- Highlight deadlock màu đỏ
- Log chi tiết mọi hành động

✨ **Tab Banker's Algorithm:**
- Safety Algorithm đầy đủ
- Resource Request Algorithm
- Validation và rollback tự động
- Dữ liệu mẫu có sẵn
- Output chi tiết từng bước

## License

Dự án này được thực hiện cho mục đích học tập (Bài tập lớn môn Hệ điều hành)