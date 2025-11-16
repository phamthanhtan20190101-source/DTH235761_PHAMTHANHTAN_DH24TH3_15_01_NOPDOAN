# student_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import pyodbc
from datetime import datetime
import re
# Lấy chuỗi kết nối
try:
    from db_connector import CONNECTION_STRING
except ImportError:
     messagebox.showerror("Lỗi Khởi tạo", "Không tìm thấy file db_connector.py.")
     exit()

# Import font
try:
    from app_styles import (FONT_TITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON, 
                            FONT_POPUP_TITLE, FONT_TREEVIEW_HEADING, FONT_TREEVIEW_CONTENT)
except ImportError:
    messagebox.showerror("Lỗi Khởi tạo Style", "Không tìm thấy file app_styles.py.")
    exit()

# -------------------------------------------------------------------
# LỚP POP-UP ĐỂ SINH VIÊN XEM LỊCH SỬ (ĐÃ SỬA)
# -------------------------------------------------------------------
class StudentPaymentHistoryWindow(tk.Toplevel):
    def __init__(self, parent, mssv):
        super().__init__(parent)
        self.mssv = mssv
        self.title(f"Lịch sử đóng tiền của bạn")
        self.geometry("700x400") 
        self.grab_set()
        self.transient(parent)

        tk.Label(self, text=f"LỊCH SỬ ĐÓNG TIỀN CỦA BẠN", font=FONT_POPUP_TITLE, fg="#0052cc").pack(pady=10)

        tree_frame = tk.Frame(self, padx=10, pady=10)
        tree_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("History.Treeview.Heading", font=FONT_TREEVIEW_HEADING)
        style.configure("History.Treeview", font=FONT_TREEVIEW_CONTENT, rowheight=25)
        
        # Xóa cột 'loaitien'
        columns = ('thangnam', 'sotien', 'ngaydong')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style="History.Treeview")
        
        self.tree.heading('thangnam', text='Đóng cho Tháng/Năm')
        self.tree.heading('sotien', text='Số Tiền (VNĐ)')
        self.tree.heading('ngaydong', text='Ngày đóng')
        
        self.tree.column('thangnam', width=150, anchor="center")
        self.tree.column('sotien', width=150, anchor="e") 
        self.tree.column('ngaydong', width=150, anchor="center")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.load_history()

    def load_history(self):
        conn = None
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            # Xóa LoaiTien khỏi câu SQL
            sql = "SELECT ThangDongTien, NamDongTien, SoTien, NgayDong FROM LichSuDongTien WHERE MSSV = ? ORDER BY NamDongTien DESC, ThangDongTien DESC"
            cursor.execute(sql, self.mssv)
            rows = cursor.fetchall()
            
            for row in rows:
                thangnam = f"{row.ThangDongTien}/{row.NamDongTien}"
                sotien = "{:,.0f}".format(row.SoTien)
                ngaydong = row.NgayDong.strftime('%d/%m/%Y')
                # Xóa loaitien khỏi values
                self.tree.insert('', 'end', values=(thangnam, sotien, ngaydong))
                
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải lịch sử.\n{ex}", parent=self)
        finally:
            if conn: conn.close()
            
# -------------------------------------------------------------------
# LỚP POP-UP DÙNG ĐỂ THAY ĐỔI THÔNG TIN (Giữ nguyên)
# -------------------------------------------------------------------
class ChangeInfoWindow(tk.Toplevel):
    def __init__(self, parent, student_id, current_sdt):
        super().__init__(parent); self.parent = parent; self.student_id = student_id
        self.title("Đổi thông tin"); self.geometry("400x320"); self.grab_set(); self.transient(parent)
        self.sdt_var = tk.StringVar(value=current_sdt); self.new_pass_var = tk.StringVar(); self.confirm_pass_var = tk.StringVar(); self.show_pass_var = tk.BooleanVar()
        main_frame = tk.Frame(self, pady=20); main_frame.pack(expand=True)
        tk.Label(main_frame, text="THÔNG TIN CÁ NHÂN", font=FONT_POPUP_TITLE, fg="#0052cc").pack(pady=(0, 20))
        form_frame = tk.Frame(main_frame); form_frame.pack(pady=5, padx=10)
        tk.Label(form_frame, text="Số điện thoại:", font=FONT_LABEL).grid(row=0, column=0, sticky="e", padx=5, pady=8)
        sdt_entry = tk.Entry(form_frame, textvariable=self.sdt_var, font=FONT_ENTRY, relief="solid", bd=1, width=25); sdt_entry.grid(row=0, column=1, sticky="w", padx=5, pady=8)
        tk.Label(form_frame, text="Mật khẩu mới:", font=FONT_LABEL).grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.pass_entry = tk.Entry(form_frame, textvariable=self.new_pass_var, show="*", font=FONT_ENTRY, relief="solid", bd=1, width=25); self.pass_entry.grid(row=1, column=1, sticky="w", padx=5, pady=8)
        tk.Label(form_frame, text="Xác nhận mật khẩu:", font=FONT_LABEL).grid(row=2, column=0, sticky="e", padx=5, pady=8)
        self.confirm_entry = tk.Entry(form_frame, textvariable=self.confirm_pass_var, show="*", font=FONT_ENTRY, relief="solid", bd=1, width=25); self.confirm_entry.grid(row=2, column=1, sticky="w", padx=5, pady=8)
        check_frame = tk.Frame(main_frame); check_frame.pack()
        show_pass_check = tk.Checkbutton(check_frame, text="Hiện mật khẩu", font=("Times New Roman", 10), variable=self.show_pass_var, command=self._toggle_password_visibility); show_pass_check.pack(pady=5)
        save_button = tk.Button(main_frame, text="Cập nhật thông tin", font=FONT_BUTTON, bg="#90EE90", fg="black", width=20, height=1, relief="solid", bd=1, command=self.save_changes); save_button.pack(pady=15)
    def _toggle_password_visibility(self): show = "" if self.show_pass_var.get() else "*"; self.pass_entry.config(show=show); self.confirm_entry.config(show=show)
    def _get_db_connection(self):
        try: return pyodbc.connect(CONNECTION_STRING)
        except pyodbc.Error as ex: messagebox.showerror("Lỗi kết nối CSDL", f"Không thể kết nối.\n{ex}", parent=self); return None
    def save_changes(self):
        new_sdt = self.sdt_var.get().strip(); new_pass = self.new_pass_var.get(); confirm_pass = self.confirm_pass_var.get()
        """if not new_sdt: messagebox.showwarning("Thiếu thông tin", "SĐT không được để trống.", parent=self); return"""
        if not new_sdt:
            messagebox.showwarning("Thiếu thông tin", "SĐT không được để trống.", parent=self)
            return
        # Kiểm tra định dạng SĐT
        if not re.match(r'^0\d{9}$', new_sdt):
            messagebox.showwarning("Lỗi Số điện thoại", "Số điện thoại không hợp lệ.\n(Phải bắt đầu bằng '0' và có đúng 10 chữ số).", parent=self)
            return
        conn = self._get_db_connection();
        if not conn: return
        try:
            cursor = conn.cursor(); conn.autocommit = False
            cursor.execute("UPDATE SinhVien SET SDT=? WHERE MSSV=?", new_sdt, self.student_id)
            if new_pass:
                if new_pass != confirm_pass: messagebox.showwarning("Mật khẩu không khớp", "Mật khẩu không giống nhau.", parent=self); conn.rollback(); return
                cursor.execute("UPDATE TaiKhoan SET MatKhau=? WHERE TenDangNhap=?", new_pass, self.student_id)
            conn.commit(); messagebox.showinfo("Thành công", "Cập nhật thành công!", parent=self); self.parent.sdt_var.set(new_sdt); self.destroy()
        except pyodbc.Error as ex: conn.rollback(); messagebox.showerror("Lỗi Cập nhật", f"Có lỗi xảy ra: {ex}", parent=self)
        finally:
            if conn: conn.close()
            
# -------------------------------------------------------------------
# LỚP FORM CHÍNH CỦA SINH VIÊN (ĐÃ SỬA)
# -------------------------------------------------------------------
class StudentForm:
    def __init__(self, login_window, student_id, login_form_instance):
        self.login_window = login_window
        self.student_id = student_id
        self.login_form = login_form_instance 

        self.window = tk.Toplevel(login_window)
        self.window.title(f"Sinh viên")
        self.window.geometry("750x650") 
        self.window.protocol("WM_DELETE_WINDOW", self.confirm_exit) 

        # --- SỬA: Gộp 2 biến trạng thái thành 1 ---
        self.mssv_var = tk.StringVar(); self.hoten_var = tk.StringVar(); self.lop_var = tk.StringVar(); self.sdt_var = tk.StringVar(); self.gioitinh_var = tk.StringVar(); self.ngaysinh_var = tk.StringVar(); self.ngayvao_var = tk.StringVar(); self.quequan_var = tk.StringVar(); self.maphong_var = tk.StringVar()
        self.payment_status_var = tk.StringVar() # Chỉ dùng 1 biến
        
        self.create_widgets()
        self.load_student_data()

    def on_closing(self): self.window.destroy(); self.login_window.destroy()
    def confirm_exit(self):
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát?", parent=self.window): self.on_closing()
    def action_logout(self): self.window.destroy(); self.login_form.clear_credentials(); self.login_window.deiconify()
    def _get_db_connection(self):
        try: return pyodbc.connect(CONNECTION_STRING)
        except pyodbc.Error as ex: messagebox.showerror("Lỗi kết nối CSDL", f"Không thể kết nối.\n{ex}"); return None

    # --- HÀM ĐÃ SỬA: Gộp 2 nhãn thành 1 ---
    def create_widgets(self):
        container = tk.Frame(self.window); container.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(container, text="Thông tin sinh viên", font=FONT_TITLE, fg="black").grid(row=0, column=0, columnspan=3, pady=(0, 25))
        container.grid_columnconfigure(0, weight=1, minsize=180); container.grid_columnconfigure(1, weight=3); container.grid_columnconfigure(2, weight=1, minsize=200)
        
        # Sửa lại danh sách nhãn
        labels_info = [
            ("MSSV:", self.mssv_var), ("Họ Tên:", self.hoten_var), ("Lớp:", self.lop_var), 
            ("SĐT:", self.sdt_var), ("Giới Tính:", self.gioitinh_var), ("Ngày Sinh:", self.ngaysinh_var), 
            ("Ngày Vào:", self.ngayvao_var), ("Quê Quán:", self.quequan_var), ("Mã Phòng:", self.maphong_var),
            ("Tiền KTX (tháng này):", self.payment_status_var) # Sửa nhãn
        ]
        
        for i, (text, var) in enumerate(labels_info):
            row_num = i + 1
            tk.Label(container, text=text, font=FONT_LABEL).grid(row=row_num, column=0, sticky="w", padx=10, pady=8) 
            data_label = tk.Label(container, textvariable=var, font=FONT_ENTRY, anchor="w", justify="left", borderwidth=1, relief="solid", padx=5); data_label.grid(row=row_num, column=1, sticky="ew", padx=10, pady=8)

        button_container = tk.Frame(container); button_container.grid(row=1, column=2, rowspan=5, sticky="n", padx=20, pady=10)
        
        btn_change_info = tk.Button(button_container, text="Đổi thông tin cá nhân", font=FONT_BUTTON, bg="#f0f0f0", fg="black", width=18, height=1, relief="solid", bd=1, command=self.open_change_info_popup); btn_change_info.pack(pady=10)
        
        # Thêm nút Xem Lịch sử
        btn_view_history = tk.Button(button_container, text="Xem lịch sử đóng tiền", font=FONT_BUTTON, bg="#17a2b8", fg="white", width=18, height=1, relief="solid", bd=1, command=self.open_history_window); btn_view_history.pack(pady=10)
        
        btn_exit = tk.Button(button_container, text="Thoát", font=FONT_BUTTON, bg="#f0f0f0", fg="black", width=18, height=1, relief="solid", bd=1, command=self.confirm_exit); btn_exit.pack(pady=10) 
        btn_logout = tk.Button(button_container, text="Đăng xuất", font=FONT_BUTTON, bg="#ffc107", fg="black", width=18, height=1, relief="solid", bd=1, command=self.action_logout); btn_logout.pack(pady=10)

    # --- HÀM ĐÃ SỬA: Tải trạng thái cho 1 loại tiền TỔNG ---
    def load_student_data(self):
        conn = self._get_db_connection();
        if not conn: return
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        try:
            cursor = conn.cursor()
            # Lấy thông tin SV và thông tin Phòng (Giá, Tiền điện nước)
            sql_sv = """
                SELECT SV.*, P.Gia, P.TienDienNuoc
                FROM SinhVien SV
                LEFT JOIN Phong P ON SV.MaPhong = P.MaPhong
                WHERE SV.MSSV = ?
            """
            cursor.execute(sql_sv, self.student_id)
            sv_data = cursor.fetchone()
            
            if not sv_data:
                messagebox.showerror("Lỗi Dữ liệu", f"Không tìm thấy dữ liệu cho: {self.student_id}"); self.window.after(100, self.on_closing)
                return

            # Lấy lịch sử đóng tiền của tháng này (Xóa LoaiTien)
            sql_payment = "SELECT MaThanhToan FROM LichSuDongTien WHERE MSSV = ? AND ThangDongTien = ? AND NamDongTien = ?"
            cursor.execute(sql_payment, (self.student_id, current_month, current_year))
            payments = cursor.fetchall() # Kiểm tra xem có bản ghi nào không
            
            # Cập nhật giao diện
            self.mssv_var.set(sv_data.MSSV); self.hoten_var.set(sv_data.HoTen); self.lop_var.set(sv_data.Lop or ""); self.sdt_var.set(sv_data.SDT or ""); self.gioitinh_var.set(sv_data.GioiTinh or "")
            self.ngaysinh_var.set(sv_data.NgaySinh.strftime('%d/%m/%Y') if sv_data.NgaySinh else "")
            self.ngayvao_var.set(sv_data.NgayVao.strftime('%d/%m/%Y') if sv_data.NgayVao else "")
            self.quequan_var.set(sv_data.QueQuan or ""); self.maphong_var.set(sv_data.MaPhong or "")

            # Cập nhật trạng thái tiền (gộp)
            gia_phong = sv_data.Gia if sv_data.Gia else 0.0
            gia_dien_nuoc = sv_data.TienDienNuoc if sv_data.TienDienNuoc else 0.0
            gia_tong = gia_phong + gia_dien_nuoc
            
            if payments: # Nếu có bất kỳ bản ghi nào, là đã đóng
                self.payment_status_var.set("Đã đóng")
            else:
                self.payment_status_var.set(f"Chưa đóng ({gia_tong:,.0f} VNĐ)")

        except pyodbc.Error as ex: 
            messagebox.showerror("Lỗi Truy vấn", f"Lỗi tải dữ liệu.\n{ex}")
        finally:
            if conn: conn.close()

    # --- HÀM MỚI: Mở pop-up xem lịch sử ---
    def open_history_window(self):
        StudentPaymentHistoryWindow(self.window, self.student_id)

    def open_change_info_popup(self): 
        current_sdt = self.sdt_var.get(); 
        ChangeInfoWindow(self.window, self.student_id, current_sdt)