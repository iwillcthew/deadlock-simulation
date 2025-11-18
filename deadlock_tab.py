"""
Tab mô phỏng Deadlock với Resource Allocation Graph
Mô phỏng tự động từ kịch bản có sẵn
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from collections import defaultdict, deque
import time


class DeadlockTab:
    """Tab mô phỏng Deadlock"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Cấu trúc dữ liệu
        self.num_processes = 4
        self.num_resources = 3
        self.processes = [f"P{i}" for i in range(self.num_processes)]
        self.resources = [f"R{i}" for i in range(self.num_resources)]
        
        # Trạng thái tài nguyên: resource -> process đang giữ (None nếu rảnh)
        self.resource_holder = {r: None for r in self.resources}
        
        # Request edges: process -> list of resources đang yêu cầu
        self.request_edges = defaultdict(list)
        
        # Allocation edges: process -> list of resources đang giữ
        self.allocation_edges = defaultdict(list)
        
        # Trạng thái tiến trình
        self.process_status = {p: "Ready" for p in self.processes}
        
        # Deadlock detection
        self.deadlocked_processes = set()
        self.deadlocked_resources = set()
        
        # Kịch bản mô phỏng
        self.scenario = []
        self.current_step = 0
        self.is_running = False
        self.simulation_speed = 1000  # ms
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel: Scenario Input and Controls
        left_panel = ttk.LabelFrame(main_frame, text="Kịch bản mô phỏng", padding=10)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Scenario input section
        input_frame = ttk.LabelFrame(left_panel, text="Nhập kịch bản", padding=10)
        input_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(input_frame, text="Định dạng: <action> <process> <resource>").pack(anchor='w', pady=(0, 5))
        ttk.Label(input_frame, text="Ví dụ: allocate P0 R0, request P1 R1, release P0 R0").pack(anchor='w', pady=(0, 5))
        
        self.scenario_text = scrolledtext.ScrolledText(input_frame, height=12, width=35)
        self.scenario_text.pack(fill='both', expand=True, pady=5)
        
        # Sample data buttons
        sample_frame = ttk.Frame(input_frame)
        sample_frame.pack(fill='x', pady=5)
        
        ttk.Button(sample_frame, text="Mẫu: Deadlock", 
                  command=self.load_deadlock_sample).pack(side='left', padx=2)
        ttk.Button(sample_frame, text="Mẫu: Không Deadlock", 
                  command=self.load_no_deadlock_sample).pack(side='left', padx=2)
        
        ttk.Button(input_frame, text="Tải kịch bản", 
                  command=self.load_scenario, width=20).pack(pady=5)
        
        # Simulation controls
        control_frame = ttk.LabelFrame(left_panel, text="Điều khiển mô phỏng", padding=10)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(control_frame, text="Tốc độ (ms):").grid(row=0, column=0, sticky='w', pady=5)
        self.speed_var = tk.IntVar(value=1000)
        speed_spinbox = ttk.Spinbox(control_frame, from_=100, to=3000, increment=100,
                                     textvariable=self.speed_var, width=10)
        speed_spinbox.grid(row=0, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.btn_start = ttk.Button(btn_frame, text="▶ Bắt đầu", 
                                    command=self.start_simulation, width=12)
        self.btn_start.pack(side='left', padx=2)
        
        self.btn_pause = ttk.Button(btn_frame, text="⏸ Tạm dừng", 
                                    command=self.pause_simulation, width=12, state='disabled')
        self.btn_pause.pack(side='left', padx=2)
        
        self.btn_step = ttk.Button(btn_frame, text="→ Bước tiếp", 
                                  command=self.step_forward, width=12)
        self.btn_step.pack(side='left', padx=2)
        
        ttk.Button(control_frame, text="↻ Reset", 
                  command=self.reset, width=20).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Progress info
        self.progress_label = ttk.Label(control_frame, text="Bước: 0/0", foreground='blue')
        self.progress_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Right panel: Visualization
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Canvas for graph visualization
        canvas_frame = ttk.LabelFrame(right_panel, text="Resource Allocation Graph", padding=10)
        canvas_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=600, height=400)
        self.canvas.pack(fill='both', expand=True)
        
        # Status and log
        status_frame = ttk.LabelFrame(right_panel, text="Trạng thái & Log", padding=10)
        status_frame.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(status_frame, height=10, width=70)
        self.log_text.pack(fill='both', expand=True)
        
        # Initial draw
        self.draw_graph()
        self.log("Hệ thống khởi tạo sẵn sàng. Nhập kịch bản để bắt đầu mô phỏng.")
    
    def load_deadlock_sample(self):
        """Load kịch bản mẫu có deadlock"""
        sample = """allocate P0 R0
allocate P1 R1
allocate P2 R2
allocate P3 R3
request P0 R1
request P1 R2
request P2 R3
request P3 R0"""
        
        self.scenario_text.delete(1.0, tk.END)
        self.scenario_text.insert(1.0, sample)
        self.log("Đã load kịch bản mẫu: Deadlock (4 processes, chu trình 4)")
    
    def load_no_deadlock_sample(self):
        """Load kịch bản mẫu không có deadlock"""
        sample = """allocate P0 R0
allocate P1 R1
allocate P2 R2
request P0 R1
release P1 R1
request P1 R2
release P2 R2
release P0 R0
release P0 R1
allocate P3 R0
allocate P4 R3
request P3 R3
release P4 R3
release P1 R2
release P3 R0
release P3 R3"""
        
        self.scenario_text.delete(1.0, tk.END)
        self.scenario_text.insert(1.0, sample)
        self.log("Đã load kịch bản mẫu: Không có Deadlock (5 processes, giải phóng đúng lúc)")
    
    def load_scenario(self):
        """Đọc và parse kịch bản từ text input"""
        text = self.scenario_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập kịch bản!")
            return
        
        self.scenario = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) != 3:
                messagebox.showerror("Lỗi", 
                    f"Dòng {line_num}: Định dạng không đúng!\n"
                    f"Cần: <action> <process> <resource>\n"
                    f"Có: {line}")
                return
            
            action, process, resource = parts
            action = action.lower()
            
            if action not in ['allocate', 'request', 'release']:
                messagebox.showerror("Lỗi", 
                    f"Dòng {line_num}: Action không hợp lệ '{action}'!\n"
                    f"Chỉ chấp nhận: allocate, request, release")
                return
            
            # Validate process and resource exist
            if process not in self.processes:
                # Try to add if needed
                if process.startswith('P'):
                    try:
                        idx = int(process[1:])
                        while idx >= len(self.processes):
                            self.processes.append(f"P{len(self.processes)}")
                            self.process_status[f"P{len(self.processes)-1}"] = "Ready"
                    except:
                        messagebox.showerror("Lỗi", f"Process không hợp lệ: {process}")
                        return
            
            if resource not in self.resources:
                # Try to add if needed
                if resource.startswith('R'):
                    try:
                        idx = int(resource[1:])
                        while idx >= len(self.resources):
                            self.resources.append(f"R{len(self.resources)}")
                            self.resource_holder[f"R{len(self.resources)-1}"] = None
                    except:
                        messagebox.showerror("Lỗi", f"Resource không hợp lệ: {resource}")
                        return
            
            self.scenario.append((action, process, resource))
        
        if not self.scenario:
            messagebox.showwarning("Cảnh báo", "Kịch bản trống (chỉ có comment)!")
            return
        
        self.num_processes = len(self.processes)
        self.num_resources = len(self.resources)
        self.current_step = 0
        self.progress_label.config(text=f"Bước: 0/{len(self.scenario)}")
        
        self.log(f"✓ Đã tải kịch bản: {len(self.scenario)} bước")
        self.log(f"  - Processes: {', '.join(self.processes)}")
        self.log(f"  - Resources: {', '.join(self.resources)}")
        self.reset_state()
        messagebox.showinfo("Thành công", 
            f"Đã tải kịch bản thành công!\n\n"
            f"Số bước: {len(self.scenario)}\n"
            f"Processes: {len(self.processes)}\n"
            f"Resources: {len(self.resources)}")
    
    def start_simulation(self):
        """Bắt đầu mô phỏng tự động"""
        if not self.scenario:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải kịch bản trước!")
            return
        
        if self.current_step >= len(self.scenario):
            messagebox.showinfo("Thông báo", "Kịch bản đã chạy xong!")
            return
        
        self.is_running = True
        self.btn_start.config(state='disabled')
        self.btn_pause.config(state='normal')
        self.btn_step.config(state='disabled')
        self.log("▶ Bắt đầu mô phỏng tự động...")
        
        self.run_next_step()
    
    def pause_simulation(self):
        """Tạm dừng mô phỏng"""
        self.is_running = False
        self.btn_start.config(state='normal')
        self.btn_pause.config(state='disabled')
        self.btn_step.config(state='normal')
        self.log("⏸ Tạm dừng mô phỏng")
    
    def run_next_step(self):
        """Chạy bước tiếp theo tự động"""
        if not self.is_running or self.current_step >= len(self.scenario):
            if self.current_step >= len(self.scenario):
                self.is_running = False
                self.btn_start.config(state='disabled')
                self.btn_pause.config(state='disabled')
                self.btn_step.config(state='disabled')
                self.log("✓ Mô phỏng hoàn tất!")
                
                # Check final state
                if not self.deadlocked_processes:
                    messagebox.showinfo("Kết quả", "Kịch bản chạy xong!\n\nKhông có Deadlock.")
            return
        
        self.execute_step()
        
        if self.is_running and not self.deadlocked_processes:
            # Schedule next step
            delay = self.speed_var.get()
            self.parent.after(delay, self.run_next_step)
        else:
            # Stop if deadlock detected
            if self.deadlocked_processes:
                self.pause_simulation()
    
    def step_forward(self):
        """Thực hiện một bước tiếp theo"""
        if not self.scenario:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải kịch bản trước!")
            return
        
        if self.current_step >= len(self.scenario):
            messagebox.showinfo("Thông báo", "Đã hết kịch bản!")
            return
        
        self.execute_step()
        
        if self.current_step >= len(self.scenario):
            self.btn_step.config(state='disabled')
            self.log("✓ Đã thực hiện hết các bước!")
    
    def execute_step(self):
        """Thực thi một bước trong kịch bản"""
        if self.current_step >= len(self.scenario):
            return
        
        action, process, resource = self.scenario[self.current_step]
        self.current_step += 1
        self.progress_label.config(text=f"Bước: {self.current_step}/{len(self.scenario)}")
        
        self.log(f"\n[Bước {self.current_step}] {action.upper()} {process} {resource}")
        
        if action == 'allocate':
            self.allocate(process, resource)
        elif action == 'request':
            self.request(process, resource)
        elif action == 'release':
            self.release(process, resource)
    
    def allocate(self, process, resource):
        """Cấp phát tài nguyên cho tiến trình"""
        # Kiểm tra tài nguyên có rảnh không
        if self.resource_holder[resource] is not None:
            holder = self.resource_holder[resource]
            self.log(f"  ⚠ Lỗi: {resource} đang được giữ bởi {holder}!")
            return
        
        # Cấp phát
        self.resource_holder[resource] = process
        self.allocation_edges[process].append(resource)
        self.process_status[process] = "Running"
        
        self.log(f"  ✓ Cấp phát {resource} cho {process}")
        self.draw_graph()
    
    def request(self, process, resource):
        """Tiến trình yêu cầu tài nguyên"""
        # Kiểm tra xem tài nguyên có rảnh không
        if self.resource_holder[resource] is None:
            # Tài nguyên rảnh, cấp phát ngay
            self.resource_holder[resource] = process
            self.allocation_edges[process].append(resource)
            self.process_status[process] = "Running"
            self.log(f"  ✓ {process} yêu cầu {resource} - Cấp phát ngay (tài nguyên rảnh)")
        else:
            # Tài nguyên đang bị giữ, thêm vào request edge
            holder = self.resource_holder[resource]
            if resource not in self.request_edges[process]:
                self.request_edges[process].append(resource)
            self.process_status[process] = "Blocked"
            self.log(f"  ⚠ {process} yêu cầu {resource} - Bị chặn ({resource} đang được giữ bởi {holder})")
            
            # Tự động phát hiện deadlock sau request bị chặn
            if self.detect_deadlock_silent():
                self.log(f"  🔴 DEADLOCK PHÁT HIỆN tại bước {self.current_step}!")
                # Vẽ graph trước khi hiển thị messagebox
                self.draw_graph()
                self.canvas.update()  # Force update canvas
                messagebox.showerror("DEADLOCK DETECTED!", 
                    f"WARNING: PROCESS DEADLOCK IS DETECTED!\n\n"
                    f"Đã phát hiện deadlock tại bước {self.current_step}!\n"
                    f"Chu trình: {' -> '.join(self.deadlocked_processes)}")
                return
        
        self.draw_graph()
    
    def release(self, process, resource):
        """Giải phóng tài nguyên"""
        # Kiểm tra tiến trình có đang giữ tài nguyên không
        if self.resource_holder[resource] != process:
            self.log(f"  ⚠ Lỗi: {process} không đang giữ {resource}!")
            return
        
        # Giải phóng
        self.resource_holder[resource] = None
        if resource in self.allocation_edges[process]:
            self.allocation_edges[process].remove(resource)
        
        # Kiểm tra có tiến trình nào đang chờ tài nguyên này không
        waiting_processes = [p for p, reqs in self.request_edges.items() if resource in reqs]
        
        if waiting_processes:
            # Cấp phát cho tiến trình đầu tiên đang chờ
            next_process = waiting_processes[0]
            self.resource_holder[resource] = next_process
            self.request_edges[next_process].remove(resource)
            self.allocation_edges[next_process].append(resource)
            self.process_status[next_process] = "Running"
            self.log(f"  ✓ {process} giải phóng {resource} - Cấp phát cho {next_process}")
        else:
            self.log(f"  ✓ {process} giải phóng {resource}")
        
        # Cập nhật trạng thái tiến trình
        if not self.allocation_edges[process]:
            self.process_status[process] = "Ready"
        
        # Clear deadlock nếu có
        self.deadlocked_processes.clear()
        self.deadlocked_resources.clear()
        
        self.draw_graph()
    
    def detect_deadlock_silent(self):
        """Phát hiện deadlock (không hiển thị dialog)"""
        # Xây dựng wait-for graph (process -> process)
        wait_for = defaultdict(set)
        
        for process, requested_resources in self.request_edges.items():
            for resource in requested_resources:
                holder = self.resource_holder.get(resource)
                if holder and holder != process:
                    wait_for[process].add(holder)
        
        # Phát hiện chu trình bằng DFS
        def has_cycle_dfs(node, visited, rec_stack, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in wait_for[node]:
                if neighbor not in visited:
                    if has_cycle_dfs(neighbor, visited, rec_stack, path):
                        return True
                elif neighbor in rec_stack:
                    # Tìm thấy chu trình
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:]
                    return cycle
            
            path.pop()
            rec_stack.remove(node)
            return False
        
        visited = set()
        for process in self.processes:
            if process not in visited:
                rec_stack = set()
                path = []
                result = has_cycle_dfs(process, visited, rec_stack, path)
                if result:
                    # Deadlock phát hiện
                    cycle = result if isinstance(result, list) else path
                    self.deadlocked_processes = set(cycle)
                    
                    # Tìm các tài nguyên liên quan đến deadlock
                    for p in cycle:
                        for r in self.request_edges[p]:
                            self.deadlocked_resources.add(r)
                        for r in self.allocation_edges[p]:
                            self.deadlocked_resources.add(r)
                    
                    return True
        
        return False
    
    def draw_graph(self):
        """Vẽ Resource Allocation Graph"""
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 600
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 400
        
        # Vị trí processes (bên trái)
        process_positions = {}
        p_spacing = height / (self.num_processes + 1)
        for i, process in enumerate(self.processes):
            x = width * 0.25
            y = p_spacing * (i + 1)
            process_positions[process] = (x, y)
        
        # Vị trí resources (bên phải)
        resource_positions = {}
        r_spacing = height / (self.num_resources + 1)
        for i, resource in enumerate(self.resources):
            x = width * 0.75
            y = r_spacing * (i + 1)
            resource_positions[resource] = (x, y)
        
        # Vẽ edges (allocation: resource -> process)
        for process, resources in self.allocation_edges.items():
            for resource in resources:
                p_x, p_y = process_positions[process]
                r_x, r_y = resource_positions[resource]
                
                color = "red" if resource in self.deadlocked_resources else "green"
                width_line = 3 if resource in self.deadlocked_resources else 2
                
                # Arrow từ resource -> process (allocation)
                self.canvas.create_line(r_x, r_y, p_x, p_y, 
                                      arrow=tk.LAST, fill=color, width=width_line)
                self.canvas.create_text((r_x + p_x) / 2, (r_y + p_y) / 2 - 10,
                                      text="alloc", fill=color, font=("Arial", 8))
        
        # Vẽ edges (request: process -> resource)
        for process, resources in self.request_edges.items():
            for resource in resources:
                p_x, p_y = process_positions[process]
                r_x, r_y = resource_positions[resource]
                
                color = "red" if process in self.deadlocked_processes else "orange"
                width_line = 3 if process in self.deadlocked_processes else 2
                
                # Arrow từ process -> resource (request)
                self.canvas.create_line(p_x, p_y, r_x, r_y, 
                                      arrow=tk.LAST, fill=color, width=width_line, dash=(4, 2))
                self.canvas.create_text((r_x + p_x) / 2, (r_y + p_y) / 2 + 10,
                                      text="request", fill=color, font=("Arial", 8))
        
        # Vẽ processes (circles)
        for process, (x, y) in process_positions.items():
            color = "red" if process in self.deadlocked_processes else "lightblue"
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, 
                                   fill=color, outline="black", width=2)
            self.canvas.create_text(x, y, text=process, font=("Arial", 12, "bold"))
            
            # Hiển thị trạng thái
            status = self.process_status[process]
            status_color = "green" if status == "Running" else "gray"
            self.canvas.create_text(x, y + 45, text=status, 
                                   fill=status_color, font=("Arial", 9))
        
        # Vẽ resources (squares)
        for resource, (x, y) in resource_positions.items():
            color = "red" if resource in self.deadlocked_resources else "lightyellow"
            self.canvas.create_rectangle(x - 25, y - 25, x + 25, y + 25, 
                                        fill=color, outline="black", width=2)
            self.canvas.create_text(x, y, text=resource, font=("Arial", 12, "bold"))
            
            # Hiển thị holder
            holder = self.resource_holder[resource]
            holder_text = holder if holder else "Free"
            holder_color = "blue" if holder else "green"
            self.canvas.create_text(x, y + 40, text=holder_text, 
                                   fill=holder_color, font=("Arial", 9))
        
        # Chú thích
        legend_y = 20
        self.canvas.create_text(20, legend_y, text="Chú thích:", 
                              anchor='w', font=("Arial", 10, "bold"))
        self.canvas.create_line(20, legend_y + 20, 60, legend_y + 20, 
                              arrow=tk.LAST, fill="green", width=2)
        self.canvas.create_text(70, legend_y + 20, text="Allocation", 
                              anchor='w', font=("Arial", 9))
        self.canvas.create_line(20, legend_y + 40, 60, legend_y + 40, 
                              arrow=tk.LAST, fill="orange", width=2, dash=(4, 2))
        self.canvas.create_text(70, legend_y + 40, text="Request", 
                              anchor='w', font=("Arial", 9))
        self.canvas.create_line(20, legend_y + 60, 60, legend_y + 60, 
                              arrow=tk.LAST, fill="red", width=3)
        self.canvas.create_text(70, legend_y + 60, text="Deadlock", 
                              anchor='w', font=("Arial", 9))
    
    def reset_state(self):
        """Reset trạng thái hệ thống (giữ kịch bản)"""
        self.resource_holder = {r: None for r in self.resources}
        self.request_edges = defaultdict(list)
        self.allocation_edges = defaultdict(list)
        self.process_status = {p: "Ready" for p in self.processes}
        self.deadlocked_processes.clear()
        self.deadlocked_resources.clear()
        self.draw_graph()
    
    def reset(self):
        """Reset toàn bộ hệ thống"""
        self.scenario = []
        self.current_step = 0
        self.is_running = False
        self.progress_label.config(text="Bước: 0/0")
        
        self.processes = [f"P{i}" for i in range(4)]
        self.resources = [f"R{i}" for i in range(3)]
        self.num_processes = 4
        self.num_resources = 3
        
        self.reset_state()
        
        self.btn_start.config(state='normal')
        self.btn_pause.config(state='disabled')
        self.btn_step.config(state='normal')
        
        self.log_text.delete(1.0, tk.END)
        self.log("Hệ thống đã được reset.")
        self.draw_graph()
    
    def log(self, message):
        """Ghi log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.parent.update()  # Update GUI immediately
