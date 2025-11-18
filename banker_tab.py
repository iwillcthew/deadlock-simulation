"""
Tab giải thuật Banker để tránh Deadlock
Hiện thực Safety Algorithm và Resource Request Algorithm
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import copy


class BankerTab:
    """Tab Banker's Algorithm"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Dữ liệu hệ thống
        self.num_processes = 5
        self.num_resources = 3
        
        # Ma trận và vector
        self.available = None
        self.max_matrix = None
        self.allocation = None
        self.need = None
        
        # Khởi tạo với dữ liệu mẫu
        self.init_sample_data()
        
        self.setup_ui()
        
    def init_sample_data(self):
        """Khởi tạo dữ liệu mẫu (ví dụ từ sách giáo trình)"""
        # Available resources (ví dụ: 3 loại tài nguyên)
        self.available = [3, 3, 2]
        
        # Max matrix (nhu cầu tối đa của mỗi tiến trình)
        self.max_matrix = [
            [7, 5, 3],  # P0
            [3, 2, 2],  # P1
            [9, 0, 2],  # P2
            [2, 2, 2],  # P3
            [4, 3, 3]   # P4
        ]
        
        # Allocation matrix (đã cấp phát)
        self.allocation = [
            [0, 1, 0],  # P0
            [2, 0, 0],  # P1
            [3, 0, 2],  # P2
            [2, 1, 1],  # P3
            [0, 0, 2]   # P4
        ]
        
        # Tính Need = Max - Allocation
        self.calculate_need()
    
    def calculate_need(self):
        """Tính ma trận Need = Max - Allocation"""
        self.need = []
        for i in range(self.num_processes):
            need_row = []
            for j in range(self.num_resources):
                need_row.append(self.max_matrix[i][j] - self.allocation[i][j])
            self.need.append(need_row)
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Top panel: Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Cấu hình hệ thống", padding=10)
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Process and Resource count
        count_frame = ttk.Frame(config_frame)
        count_frame.pack(fill='x', pady=5)
        
        ttk.Label(count_frame, text="Số tiến trình (n):").pack(side='left', padx=5)
        self.process_entry = ttk.Entry(count_frame, width=5)
        self.process_entry.insert(0, str(self.num_processes))
        self.process_entry.pack(side='left', padx=5)
        
        ttk.Label(count_frame, text="Số loại tài nguyên (m):").pack(side='left', padx=5)
        self.resource_entry = ttk.Entry(count_frame, width=5)
        self.resource_entry.insert(0, str(self.num_resources))
        self.resource_entry.pack(side='left', padx=5)
        
        ttk.Button(count_frame, text="Khởi tạo ma trận", 
                  command=self.init_matrices).pack(side='left', padx=10)
        ttk.Button(count_frame, text="Dữ liệu mẫu", 
                  command=self.load_sample).pack(side='left', padx=5)
        
        # Middle panel: Matrices
        matrix_frame = ttk.Frame(main_frame)
        matrix_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Available vector
        available_frame = ttk.LabelFrame(matrix_frame, text="Available", padding=10)
        available_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        self.available_text = scrolledtext.ScrolledText(available_frame, height=3, width=30)
        self.available_text.pack(fill='both', expand=True)
        
        # Max matrix
        max_frame = ttk.LabelFrame(matrix_frame, text="Max Matrix", padding=10)
        max_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.max_text = scrolledtext.ScrolledText(max_frame, height=8, width=30)
        self.max_text.pack(fill='both', expand=True)
        
        # Allocation matrix
        alloc_frame = ttk.LabelFrame(matrix_frame, text="Allocation Matrix", padding=10)
        alloc_frame.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        
        self.alloc_text = scrolledtext.ScrolledText(alloc_frame, height=8, width=30)
        self.alloc_text.pack(fill='both', expand=True)
        
        # Need matrix (read-only)
        need_frame = ttk.LabelFrame(matrix_frame, text="Need Matrix (tự động tính)", padding=10)
        need_frame.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
        
        self.need_text = scrolledtext.ScrolledText(need_frame, height=8, width=30)
        self.need_text.pack(fill='both', expand=True)
        
        matrix_frame.columnconfigure(0, weight=1)
        matrix_frame.columnconfigure(1, weight=1)
        matrix_frame.columnconfigure(2, weight=1)
        matrix_frame.rowconfigure(1, weight=1)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Cập nhật dữ liệu", 
                  command=self.update_data).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Kiểm tra trạng thái an toàn", 
                  command=self.safety_check).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Yêu cầu tài nguyên", 
                  command=self.resource_request_dialog).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Reset", 
                  command=self.reset).pack(side='left', padx=5)
        
        # Bottom panel: Output
        output_frame = ttk.LabelFrame(main_frame, text="Output & Log", padding=10)
        output_frame.pack(fill='both', expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, width=100)
        self.output_text.pack(fill='both', expand=True)
        
        # Display initial data
        self.display_data()
        self.log("Banker's Algorithm đã sẵn sàng. Sử dụng dữ liệu mẫu.")
    
    def init_matrices(self):
        """Khởi tạo ma trận với kích thước mới"""
        try:
            n = int(self.process_entry.get())
            m = int(self.resource_entry.get())
            
            if n < 1 or m < 1:
                raise ValueError("Số lượng phải lớn hơn 0")
            
            self.num_processes = n
            self.num_resources = m
            
            # Khởi tạo ma trận rỗng
            self.available = [0] * m
            self.max_matrix = [[0] * m for _ in range(n)]
            self.allocation = [[0] * m for _ in range(n)]
            self.need = [[0] * m for _ in range(n)]
            
            self.display_data()
            self.log(f"Đã khởi tạo ma trận: {n} tiến trình, {m} loại tài nguyên")
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")
    
    def load_sample(self):
        """Load dữ liệu mẫu"""
        self.num_processes = 5
        self.num_resources = 3
        self.process_entry.delete(0, tk.END)
        self.process_entry.insert(0, "5")
        self.resource_entry.delete(0, tk.END)
        self.resource_entry.insert(0, "3")
        self.init_sample_data()
        self.display_data()
        self.log("Đã load dữ liệu mẫu")
    
    def display_data(self):
        """Hiển thị dữ liệu lên GUI"""
        # Available
        self.available_text.delete(1.0, tk.END)
        self.available_text.insert(tk.END, "Available = " + str(self.available))
        
        # Max
        self.max_text.delete(1.0, tk.END)
        for i, row in enumerate(self.max_matrix):
            self.max_text.insert(tk.END, f"P{i}: {row}\n")
        
        # Allocation
        self.alloc_text.delete(1.0, tk.END)
        for i, row in enumerate(self.allocation):
            self.alloc_text.insert(tk.END, f"P{i}: {row}\n")
        
        # Need
        self.need_text.delete(1.0, tk.END)
        for i, row in enumerate(self.need):
            self.need_text.insert(tk.END, f"P{i}: {row}\n")
    
    def update_data(self):
        """Cập nhật dữ liệu từ GUI"""
        try:
            # Parse Available
            available_str = self.available_text.get(1.0, tk.END).strip()
            available_str = available_str.replace("Available = ", "").strip()
            self.available = eval(available_str)
            
            # Parse Max
            max_lines = self.max_text.get(1.0, tk.END).strip().split('\n')
            self.max_matrix = []
            for line in max_lines:
                if line.strip():
                    row_str = line.split(':')[1].strip()
                    self.max_matrix.append(eval(row_str))
            
            # Parse Allocation
            alloc_lines = self.alloc_text.get(1.0, tk.END).strip().split('\n')
            self.allocation = []
            for line in alloc_lines:
                if line.strip():
                    row_str = line.split(':')[1].strip()
                    self.allocation.append(eval(row_str))
            
            # Recalculate Need
            self.calculate_need()
            self.display_data()
            
            self.log("✓ Dữ liệu đã được cập nhật")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể parse dữ liệu: {e}")
    
    def safety_check(self):
        """Chạy Safety Algorithm"""
        self.output_text.delete(1.0, tk.END)
        self.log("\n=== BẮT ĐẦU KIỂM TRA TRẠNG THÁI AN TOÀN ===\n", to_output=True)
        
        # Initialize Work and Finish
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []
        
        self.log(f"Bước 0: Khởi tạo", to_output=True)
        self.log(f"  Work = {work}", to_output=True)
        self.log(f"  Finish = {finish}\n", to_output=True)
        
        step = 1
        while len(safe_sequence) < self.num_processes:
            found = False
            
            for i in range(self.num_processes):
                if not finish[i]:
                    # Kiểm tra Need[i] <= Work
                    can_allocate = all(self.need[i][j] <= work[j] 
                                     for j in range(self.num_resources))
                    
                    if can_allocate:
                        self.log(f"Bước {step}:", to_output=True)
                        self.log(f"  Tìm thấy P{i}: Need[{i}] = {self.need[i]} <= Work = {work}", 
                               to_output=True)
                        
                        # Cấp phát
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        
                        finish[i] = True
                        safe_sequence.append(f"P{i}")
                        
                        self.log(f"  P{i} chạy xong. Work = Work + Allocation[{i}] = {work}", 
                               to_output=True)
                        self.log(f"  Finish[{i}] = True\n", to_output=True)
                        
                        found = True
                        step += 1
                        break
            
            if not found:
                # Không tìm thấy tiến trình nào có thể chạy
                self.log("=== KẾT QUẢ: KHÔNG AN TOÀN ===", to_output=True)
                self.log("Không tìm thấy tiến trình nào có thể tiếp tục!", to_output=True)
                messagebox.showwarning("Kết quả", "Trạng thái KHÔNG AN TOÀN!\n\n"
                                     "Hệ thống có thể rơi vào deadlock.")
                return False
        
        # Safe state
        sequence_str = " -> ".join(safe_sequence)
        self.log("=== KẾT QUẢ: AN TOÀN ===", to_output=True)
        self.log(f"Trạng thái an toàn!", to_output=True)
        self.log(f"Chuỗi an toàn: {sequence_str}", to_output=True)
        
        messagebox.showinfo("Kết quả", f"Trạng thái AN TOÀN!\n\n"
                          f"Chuỗi an toàn:\n{sequence_str}")
        return True
    
    def resource_request_dialog(self):
        """Hiển thị dialog yêu cầu tài nguyên"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Yêu cầu tài nguyên")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        # Process selection
        ttk.Label(dialog, text="Chọn tiến trình:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        process_var = tk.IntVar(value=0)
        process_combo = ttk.Combobox(dialog, 
                                    values=[f"P{i}" for i in range(self.num_processes)],
                                    state='readonly', width=10)
        process_combo.current(0)
        process_combo.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Request vector
        ttk.Label(dialog, text="Vector Request:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(dialog, text="(Ví dụ: [1, 0, 2])").grid(row=2, column=0, columnspan=2, padx=10, sticky='w')
        
        request_entry = ttk.Entry(dialog, width=30)
        request_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        request_entry.insert(0, "[0, 0, 0]")
        
        def submit_request():
            try:
                process_idx = int(process_combo.get()[1:])  # Lấy số từ "P0", "P1"...
                request = eval(request_entry.get())
                
                if len(request) != self.num_resources:
                    raise ValueError(f"Request phải có {self.num_resources} phần tử")
                
                dialog.destroy()
                self.process_request(process_idx, request)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {e}")
        
        ttk.Button(dialog, text="Gửi yêu cầu", command=submit_request).grid(
            row=3, column=0, columnspan=2, pady=20)
    
    def process_request(self, process_idx, request):
        """Xử lý yêu cầu tài nguyên theo Banker's Algorithm"""
        self.output_text.delete(1.0, tk.END)
        self.log(f"\n=== XỬ LÝ YÊU CẦU TÀI NGUYÊN ===", to_output=True)
        self.log(f"Tiến trình: P{process_idx}", to_output=True)
        self.log(f"Request[{process_idx}] = {request}\n", to_output=True)
        
        # Bước 1: Kiểm tra Request <= Need
        self.log("Bước 1: Kiểm tra Request[i] <= Need[i]", to_output=True)
        if not all(request[j] <= self.need[process_idx][j] for j in range(self.num_resources)):
            self.log(f"  LỖI: Request = {request} > Need[{process_idx}] = {self.need[process_idx]}", 
                   to_output=True)
            self.log("  Tiến trình yêu cầu vượt quá nhu cầu tối đa!", to_output=True)
            messagebox.showerror("Lỗi", "Request vượt quá Need!\n\n"
                               "Tiến trình yêu cầu nhiều hơn nhu cầu tối đa đã khai báo.")
            return
        self.log(f"  ✓ Request = {request} <= Need[{process_idx}] = {self.need[process_idx]}\n", 
               to_output=True)
        
        # Bước 2: Kiểm tra Request <= Available
        self.log("Bước 2: Kiểm tra Request[i] <= Available", to_output=True)
        if not all(request[j] <= self.available[j] for j in range(self.num_resources)):
            self.log(f"  LỖI: Request = {request} > Available = {self.available}", to_output=True)
            self.log(f"  P{process_idx} phải chờ (tài nguyên không đủ)!", to_output=True)
            messagebox.showwarning("Không đủ tài nguyên", 
                                 f"Request = {request}\nAvailable = {self.available}\n\n"
                                 f"P{process_idx} phải chờ!")
            return
        self.log(f"  ✓ Request = {request} <= Available = {self.available}\n", to_output=True)
        
        # Bước 3: Giả lập cấp phát
        self.log("Bước 3: Giả lập cấp phát tài nguyên", to_output=True)
        
        # Backup trạng thái hiện tại
        old_available = self.available.copy()
        old_allocation = copy.deepcopy(self.allocation)
        old_need = copy.deepcopy(self.need)
        
        # Cấp phát thử
        for j in range(self.num_resources):
            self.available[j] -= request[j]
            self.allocation[process_idx][j] += request[j]
            self.need[process_idx][j] -= request[j]
        
        self.log(f"  Available_mới = {self.available}", to_output=True)
        self.log(f"  Allocation[{process_idx}]_mới = {self.allocation[process_idx]}", to_output=True)
        self.log(f"  Need[{process_idx}]_mới = {self.need[process_idx]}\n", to_output=True)
        
        # Bước 4: Chạy Safety Algorithm
        self.log("Bước 4: Chạy Safety Algorithm với trạng thái mới", to_output=True)
        self.log("-" * 50, to_output=True)
        
        is_safe = self.run_safety_algorithm_for_request()
        
        if is_safe:
            # Chấp nhận yêu cầu
            self.log("\n" + "=" * 50, to_output=True)
            self.log("KẾT QUẢ: YÊU CẦU ĐƯỢC CHẤP NHẬN", to_output=True)
            self.log(f"Trạng thái mới là AN TOÀN", to_output=True)
            self.log(f"P{process_idx} được cấp phát {request}", to_output=True)
            
            # Cập nhật GUI
            self.display_data()
            
            messagebox.showinfo("Chấp nhận yêu cầu", 
                              f"Yêu cầu được CHẤP NHẬN!\n\n"
                              f"P{process_idx} được cấp phát {request}\n"
                              f"Trạng thái mới là AN TOÀN")
        else:
            # Từ chối yêu cầu, rollback
            self.available = old_available
            self.allocation = old_allocation
            self.need = old_need
            
            self.log("\n" + "=" * 50, to_output=True)
            self.log("KẾT QUẢ: YÊU CẦU BỊ TỪ CHỐI", to_output=True)
            self.log(f"Trạng thái mới KHÔNG AN TOÀN", to_output=True)
            self.log(f"P{process_idx} phải chờ", to_output=True)
            self.log("Rollback về trạng thái cũ", to_output=True)
            
            messagebox.showwarning("Từ chối yêu cầu", 
                                 f"Yêu cầu bị TỪ CHỐI!\n\n"
                                 f"Trạng thái mới KHÔNG AN TOÀN\n"
                                 f"P{process_idx} phải chờ")
    
    def run_safety_algorithm_for_request(self):
        """Chạy Safety Algorithm (cho request validation)"""
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []
        
        self.log(f"  Work = {work}", to_output=True)
        self.log(f"  Finish = {finish}\n", to_output=True)
        
        step = 1
        while len(safe_sequence) < self.num_processes:
            found = False
            
            for i in range(self.num_processes):
                if not finish[i]:
                    can_allocate = all(self.need[i][j] <= work[j] 
                                     for j in range(self.num_resources))
                    
                    if can_allocate:
                        self.log(f"  Bước {step}: P{i} có thể chạy (Need[{i}] = {self.need[i]} <= Work = {work})", 
                               to_output=True)
                        
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        
                        finish[i] = True
                        safe_sequence.append(f"P{i}")
                        
                        self.log(f"         Work mới = {work}", to_output=True)
                        
                        found = True
                        step += 1
                        break
            
            if not found:
                self.log("  Không tìm thấy tiến trình nào có thể chạy!", to_output=True)
                self.log("  => Trạng thái KHÔNG AN TOÀN", to_output=True)
                return False
        
        sequence_str = " -> ".join(safe_sequence)
        self.log(f"  => Trạng thái AN TOÀN", to_output=True)
        self.log(f"  Chuỗi an toàn: {sequence_str}", to_output=True)
        return True
    
    def log(self, message, to_output=False):
        """Ghi log"""
        if to_output:
            self.output_text.insert(tk.END, f"{message}\n")
            self.output_text.see(tk.END)
        else:
            self.output_text.insert(tk.END, f"{message}\n")
            self.output_text.see(tk.END)
    
    def reset(self):
        """Reset về dữ liệu mẫu"""
        self.init_sample_data()
        self.display_data()
        self.output_text.delete(1.0, tk.END)
        self.log("Đã reset về dữ liệu mẫu")
