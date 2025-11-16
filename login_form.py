# login_form.py
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

# --- Import font từ file app_styles ---
try:
    from app_styles import FONT_TITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON, FONT_CHECKBOX
except ImportError:
    messagebox.showerror("Lỗi Khởi tạo Style", "Không tìm thấy file app_styles.py.")
    exit()

# --- Import các thành phần khác ---
try:
    from db_connector import check_credentials_in_sqlserver
    from student_dashboard import StudentForm
    from admin_dashboard import AdminDashboard
except ImportError as e:
    messagebox.showerror(
        "Lỗi Khởi tạo Module",
        f"Không tìm thấy một file .py cần thiết.\n\nChi tiết lỗi: {e}\n\nVui lòng đảm bảo các file đều nằm chung một thư mục."
    )
    exit()

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập Hệ thống KTX")
        self.root.geometry("480x320")

        # --- Frame chính ---
        main_frame = tk.Frame(root, pady=20, padx=20)
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="ĐĂNG NHẬP HỆ THỐNG", font=FONT_TITLE, fg="#003399").pack(pady=(0, 25))

        # --- Frame form ---
        form_frame = tk.Frame(main_frame)
        form_frame.pack(padx=10, fill="x", expand=True)
        form_frame.grid_columnconfigure(0, weight=1); form_frame.grid_columnconfigure(1, weight=2)

        # --- Widgets ---
        tk.Label(form_frame, text="Tên đăng nhập:", font=FONT_LABEL).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.username_entry = tk.Entry(form_frame, font=FONT_ENTRY, width=30, relief="solid", bd=1)
        self.username_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        tk.Label(form_frame, text="Mật khẩu:", font=FONT_LABEL).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.password_entry = tk.Entry(form_frame, font=FONT_ENTRY, show="*", width=30, relief="solid", bd=1)
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Bind Enter key
        self.username_entry.bind("<Return>", self.validate_login_event)
        self.password_entry.bind("<Return>", self.validate_login_event)

        # Checkbox
        self.show_pass_var = tk.BooleanVar()
        show_pass_check = tk.Checkbutton(form_frame, text="Hiện Mật khẩu", font=FONT_CHECKBOX, variable=self.show_pass_var, command=self.toggle_password);
        show_pass_check.grid(row=2, column=1, sticky="e", padx=10, pady=(0, 10))

        # Login button
        login_button = tk.Button(main_frame, text="Đăng nhập", font=FONT_BUTTON, bg="#54AC57", fg="white", width=20, height=1, relief="solid", bd=1, command=self.validate_login)
        login_button.pack(pady=20)

        # --- THÊM MỚI: Đặt focus vào ô username khi mở ---
        self.username_entry.focus_set()

    def toggle_password(self):
        """Hiện/Ẩn mật khẩu."""
        show = "" if self.show_pass_var.get() else "*"
        self.password_entry.config(show=show)

    # --- THÊM MỚI: Hàm để xóa thông tin đăng nhập ---
    def clear_credentials(self):
        """Xóa nội dung ô username và password."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.show_pass_var.set(False) # Bỏ tick checkbox
        self.toggle_password()        # Ẩn lại mật khẩu
        self.username_entry.focus_set() # Đặt focus lại vào username

    def validate_login(self):
        """Kiểm tra thông tin đăng nhập và mở form tương ứng."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập cả tên đăng nhập và mật khẩu.")
            return

        user_role = check_credentials_in_sqlserver(username, password)

        if user_role == "ERROR_DB_CONNECTION":
            messagebox.showerror("Lỗi Kết nối CSDL", "Không thể kết nối đến SQL Server...")
            self.password_entry.delete(0, tk.END)
            return

        if user_role:
            self.root.withdraw() # Ẩn cửa sổ login
            if user_role == 'Sinh viên':
                # --- THAY ĐỔI: Truyền `self` (LoginForm instance) ---
                StudentForm(self.root, username, self)
            elif user_role == 'Quản lý':
                # --- THAY ĐỔI: Truyền `self` (LoginForm instance) ---
                AdminDashboard(self.root, username, self)
            else:
                messagebox.showerror("Lỗi Vai trò", f"Vai trò '{user_role}' không được hỗ trợ.")
                self.root.destroy()
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng.")
            self.password_entry.delete(0, tk.END)

    # --- THÊM MỚI: Hàm xử lý sự kiện nhấn Enter ---
    def validate_login_event(self, event):
        """Gọi hàm validate_login khi nhấn Enter."""
        self.validate_login()

# --- Điểm khởi chạy của chương trình ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root) # Tạo instance của lớp LoginForm
    root.mainloop()