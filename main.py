"""
Bài tập lớn Hệ điều hành: Mô phỏng Deadlock & Giải thuật Banker
File chính khởi tạo ứng dụng GUI
"""
import tkinter as tk
from tkinter import ttk
from deadlock_tab import DeadlockTab
from banker_tab import BankerTab


class DeadlockSimulatorApp:
    """Ứng dụng chính mô phỏng Deadlock và Banker's Algorithm"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Deadlock & Banker's Algorithm")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Tạo Notebook (Tab container)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Mô phỏng Deadlock
        self.deadlock_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.deadlock_frame, text="Mô phỏng Deadlock")
        self.deadlock_tab = DeadlockTab(self.deadlock_frame)
        
        # Tab 2: Banker's Algorithm
        self.banker_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.banker_frame, text="Banker's Algorithm")
        self.banker_tab = BankerTab(self.banker_frame)
        
        # Thêm menu bar
        self.create_menu()
        
    def create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset Deadlock Tab", 
                            command=self.reset_deadlock)
        file_menu.add_command(label="Reset Banker Tab", 
                            command=self.reset_banker)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Về chương trình", command=self.show_about)
        
    def reset_deadlock(self):
        """Reset tab Deadlock"""
        self.deadlock_tab.reset()
        
    def reset_banker(self):
        """Reset tab Banker"""
        self.banker_tab.reset()
        
    def show_about(self):
        """Hiển thị thông tin về chương trình"""
        about_window = tk.Toplevel(self.root)
        about_window.title("Về chương trình")
        about_window.geometry("400x250")
        about_window.resizable(False, False)
        
        info_text = """
        Mô phỏng Deadlock & Banker's Algorithm
        
        Bài tập lớn môn Hệ điều hành
        
        Tính năng:
        - Mô phỏng và phát hiện Deadlock
        - Giải thuật Banker để tránh Deadlock
        
        Công nghệ: Python 3 + Tkinter
        
        © 2025
        """
        
        label = tk.Label(about_window, text=info_text, 
                        justify='left', padx=20, pady=20)
        label.pack()
        
        btn_ok = ttk.Button(about_window, text="OK", 
                           command=about_window.destroy)
        btn_ok.pack(pady=10)


def main():
    """Hàm main khởi chạy ứng dụng"""
    root = tk.Tk()
    app = DeadlockSimulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
