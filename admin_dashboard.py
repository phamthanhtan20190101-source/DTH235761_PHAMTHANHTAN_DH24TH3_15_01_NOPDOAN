# admin_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont
import pyodbc
from datetime import datetime
from tkcalendar import DateEntry
import re

# --- Import font từ app_styles ---
try:
    from app_styles import (FONT_TITLE, FONT_HEADING, FONT_LABEL, FONT_ENTRY,
                            FONT_BUTTON, FONT_POPUP_TITLE, FONT_POPUP_LABEL, 
                            FONT_TREEVIEW_HEADING, FONT_TREEVIEW_CONTENT)
except ImportError:
    messagebox.showerror("Lỗi Khởi tạo Style", "Không tìm thấy file app_styles.py.")
    exit()

# Lấy chuỗi kết nối
try:
    from db_connector import CONNECTION_STRING
except ImportError:
    messagebox.showerror("Lỗi Khởi tạo", "Không tìm thấy file db_connector.py.")
    exit()

# -------------------------------------------------------------------
# LỚP POP-UP: GHI NHẬN ĐÓNG TIỀN (Giữ nguyên)
# -------------------------------------------------------------------
class LogPaymentWindow(tk.Toplevel):
    def __init__(self, parent, mssv, hoten, maphong, gia_phong, gia_dien_nuoc):
        super().__init__(parent)
        self.parent = parent
        self.mssv = mssv

        self.gia_phong = gia_phong if gia_phong else 0.0
        self.gia_dien_nuoc = gia_dien_nuoc if gia_dien_nuoc else 0.0
        self.tong_tien = self.gia_phong + self.gia_dien_nuoc

        self.title("Ghi nhận đóng tiền")
        self.geometry("500x500") 
        self.grab_set()
        self.transient(parent)

        now = datetime.now()
        self.thang_var = tk.IntVar(value=now.month)
        self.nam_var = tk.IntVar(value=now.year)
        self.ngay_dong_var = tk.StringVar(value=now.strftime('%d/%m/%Y'))
        self.so_tien_var = tk.DoubleVar(value=self.tong_tien)

        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(main_frame, text="GHI NHẬN ĐÓNG TIỀN", font=FONT_POPUP_TITLE, fg="#1a69e0").pack(pady=(0, 20))
        
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill="x")
        form_frame.grid_columnconfigure(1, weight=1) 

        tk.Label(form_frame, text="Sinh viên:", font=FONT_LABEL).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        tk.Label(form_frame, text=f"{hoten} ({mssv})", font=FONT_ENTRY, anchor="w").grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Label(form_frame, text="Phòng:", font=FONT_LABEL).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        tk.Label(form_frame, text=f"{maphong}", font=FONT_ENTRY, anchor="w").grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Separator(form_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(form_frame, text="Tiền phòng:", font=FONT_POPUP_LABEL).grid(row=3, column=0, sticky="e", padx=10, pady=2)
        tk.Label(form_frame, text=f"{self.gia_phong:,.0f} VNĐ", font=FONT_ENTRY).grid(row=3, column=1, sticky="w", padx=5)
        
        tk.Label(form_frame, text="Tiền điện nước:", font=FONT_POPUP_LABEL).grid(row=4, column=0, sticky="e", padx=10, pady=2)
        tk.Label(form_frame, text=f"{self.gia_dien_nuoc:,.0f} VNĐ", font=FONT_ENTRY).grid(row=4, column=1, sticky="w", padx=5)

        tk.Label(form_frame, text="Tổng phải đóng:", font=FONT_LABEL).grid(row=5, column=0, sticky="e", padx=10, pady=2)
        tk.Label(form_frame, text=f"{self.tong_tien:,.0f} VNĐ", font=FONT_ENTRY, fg="blue").grid(row=5, column=1, sticky="w", padx=5)
        
        ttk.Separator(form_frame, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(form_frame, text="Số tiền (thực tế):", font=FONT_LABEL).grid(row=8, column=0, sticky="e", padx=10, pady=5)
        tk.Entry(form_frame, textvariable=self.so_tien_var, font=FONT_ENTRY, relief="solid", bd=1).grid(row=8, column=1, sticky="ew", padx=5)
        
        tk.Label(form_frame, text="Ngày đóng:", font=FONT_LABEL).grid(row=9, column=0, sticky="e", padx=10, pady=5)
        DateEntry(form_frame, textvariable=self.ngay_dong_var, font=FONT_ENTRY, date_pattern='dd/mm/y').grid(row=9, column=1, sticky="ew", padx=5)

        tk.Label(form_frame, text="Đóng cho tháng:", font=FONT_LABEL).grid(row=10, column=0, sticky="e", padx=10, pady=5)
        spinbox_frame_thang = tk.Frame(form_frame)
        spinbox_frame_thang.grid(row=10, column=1, sticky="w", padx=5)
        ttk.Spinbox(spinbox_frame_thang, from_=1, to=12, textvariable=self.thang_var, font=FONT_ENTRY, width=5).pack()
        
        tk.Label(form_frame, text="Năm:", font=FONT_LABEL).grid(row=11, column=0, sticky="e", padx=10, pady=5)
        spinbox_frame_nam = tk.Frame(form_frame)
        spinbox_frame_nam.grid(row=11, column=1, sticky="w", padx=5)
        ttk.Spinbox(spinbox_frame_nam, from_=2020, to=2030, textvariable=self.nam_var, font=FONT_ENTRY, width=5).pack()

        save_button = tk.Button(main_frame, text="Lưu thanh toán", font=FONT_BUTTON, bg="#28a745", fg="white", command=self.save_payment)
        save_button.pack(pady=20)

    def dmy_to_iso(self, dmy_str):
        try: return datetime.strptime(dmy_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        except: return None

    def save_payment(self):
        thang = self.thang_var.get()
        nam = self.nam_var.get()
        so_tien = self.so_tien_var.get()
        ngay_dong_str = self.ngay_dong_var.get()
        ngay_dong_iso = self.dmy_to_iso(ngay_dong_str)

        if not ngay_dong_iso or so_tien <= 0:
            messagebox.showwarning("Thiếu thông tin", "Ngày đóng và số tiền không hợp lệ.", parent=self)
            return

        confirm_msg = f"Bạn có chắc chắn muốn ghi nhận:\n\n" \
                      f"Số tiền: {so_tien:,.0f} VNĐ\n" \
                      f"Cho tháng: {thang}/{nam}"
        
        if not messagebox.askyesno("Xác nhận thanh toán", confirm_msg, parent=self):
            return

        conn = None
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            
            sql_check = "SELECT MaThanhToan FROM LichSuDongTien WHERE MSSV=? AND ThangDongTien=? AND NamDongTien=?"
            cursor.execute(sql_check, (self.mssv, thang, nam))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", f"Sinh viên này đã đóng tiền cho tháng {thang}/{nam}.", parent=self)
                return
            
            sql_insert = "INSERT INTO LichSuDongTien (MSSV, ThangDongTien, NamDongTien, SoTien, NgayDong) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql_insert, (self.mssv, thang, nam, so_tien, ngay_dong_iso))
            
            conn.commit()
            
            messagebox.showinfo("Thành công", "Đã ghi nhận thanh toán thành công!", parent=self)
            self.parent.load_all_students() 
            self.destroy()
            
        except pyodbc.Error as ex:
            if conn: conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể lưu thanh toán.\n{ex}", parent=self)
        finally:
            if conn: conn.close()
            
# -------------------------------------------------------------------
# LỚP POP-UP: XEM LỊCH SỬ ĐÓNG TIỀN (Giữ nguyên)
# -------------------------------------------------------------------
class PaymentHistoryWindow(tk.Toplevel):
    def __init__(self, parent, mssv, hoten):
        super().__init__(parent)
        self.mssv = mssv
        self.title(f"Lịch sử đóng tiền - {hoten}")
        self.geometry("700x400") 
        self.grab_set()
        self.transient(parent)

        tk.Label(self, text=f"LỊCH SỬ ĐÓNG TIỀN\n{hoten} ({mssv})", font=FONT_POPUP_TITLE, fg="#0052cc").pack(pady=10)
        tree_frame = tk.Frame(self, padx=10, pady=10); tree_frame.pack(fill="both", expand=True)
        style = ttk.Style(); style.configure("History.Treeview.Heading", font=FONT_TREEVIEW_HEADING); style.configure("History.Treeview", font=FONT_TREEVIEW_CONTENT, rowheight=25)
        
        columns = ('thangnam', 'sotien', 'ngaydong')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style="History.Treeview")
        
        self.tree.heading('thangnam', text='Đóng cho Tháng/Năm')
        self.tree.heading('sotien', text='Số Tiền (VNĐ)')
        self.tree.heading('ngaydong', text='Ngày đóng')
        
        self.tree.column('thangnam', width=150, anchor="center")
        self.tree.column('sotien', width=150, anchor="e") 
        self.tree.column('ngaydong', width=150, anchor="center")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=v_scroll.set); v_scroll.pack(side="right", fill="y"); self.tree.pack(fill="both", expand=True)
        self.load_history()

    def load_history(self):
        conn = None
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            cursor = conn.cursor()
            sql = "SELECT ThangDongTien, NamDongTien, SoTien, NgayDong FROM LichSuDongTien WHERE MSSV = ? ORDER BY NamDongTien DESC, ThangDongTien DESC"
            cursor.execute(sql, self.mssv)
            rows = cursor.fetchall()
            
            for row in rows:
                thangnam = f"{row.ThangDongTien}/{row.NamDongTien}"
                sotien = "{:,.0f}".format(row.SoTien)
                ngaydong = row.NgayDong.strftime('%d/%m/%Y')
                self.tree.insert('', 'end', values=(thangnam, sotien, ngaydong))
                
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải lịch sử.\n{ex}", parent=self)
        finally:
            if conn: conn.close()

# -------------------------------------------------------------------
# LỚP ADMIN DASHBOARD CHÍNH
# -------------------------------------------------------------------
class AdminDashboard:
    def __init__(self, login_window, admin_username, login_form_instance):
        self.login_window = login_window; self.admin_username = admin_username; self.login_form = login_form_instance 
        self.window = tk.Toplevel(login_window); self.window.title(f"Quản lý Ký túc xá ({admin_username})"); self.window.geometry("1300x700") 
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.mssv_var = tk.StringVar(); self.hoten_var = tk.StringVar(); self.lop_var = tk.StringVar(); self.sdt_var = tk.StringVar(); self.gioitinh_var = tk.StringVar(); self.ngaysinh_var = tk.StringVar(); self.ngayvao_var = tk.StringVar(); self.quequan_var = tk.StringVar(); self.maphong_var = tk.StringVar(); self.search_var = tk.StringVar(); self.search_room_var = tk.StringVar()
        self.payment_status_var = tk.StringVar() # Biến gộp
        
        self.sort_column = "NgayVao"; self.sort_order = "ASC"
        
        main_frame = tk.Frame(self.window); main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(main_frame, text="QUẢN LÝ SINH VIÊN", font=FONT_TITLE, fg="#0052cc").pack(pady=(0, 15))
        
        self.create_input_frame(main_frame)
        self.create_button_frame(main_frame)
        self.create_search_frame(main_frame)
        self.create_treeview_frame(main_frame)
        
        self._load_all_rooms_to_search_combo()
        self.load_all_students()
        self.toggle_button_state('init')

    def on_closing(self): self.window.destroy(); self.login_window.destroy()
    def _get_db_connection(self):
        try: return pyodbc.connect(CONNECTION_STRING)
        except pyodbc.Error as ex: messagebox.showerror("Lỗi kết nối CSDL", f"Không thể kết nối.\n{ex}"); return None

    # --- HÀM ĐÃ SỬA: Bố cục "Thông tin chi tiết" ---
    def create_input_frame(self, parent):
        input_frame = tk.LabelFrame(parent, text="Thông tin chi tiết", font=FONT_HEADING, padx=15, pady=10); input_frame.pack(fill="x", pady=5)
        
        input_frame.grid_columnconfigure(1, weight=2) 
        input_frame.grid_columnconfigure(3, weight=2)
        input_frame.grid_columnconfigure(5, weight=1)

        tk.Label(input_frame, text="Mã số (MSSV):", font=FONT_LABEL).grid(row=0, column=0, sticky="w", padx=10, pady=7); self.mssv_entry = tk.Entry(input_frame, textvariable=self.mssv_var, font=FONT_ENTRY); self.mssv_entry.grid(row=0, column=1, padx=10, pady=7, sticky="ew")
        tk.Label(input_frame, text="Họ tên:", font=FONT_LABEL).grid(row=0, column=2, sticky="w", padx=10, pady=7); self.hoten_entry = tk.Entry(input_frame, textvariable=self.hoten_var, font=FONT_ENTRY); self.hoten_entry.grid(row=0, column=3, padx=10, pady=7, sticky="ew")
        tk.Label(input_frame, text="Phái:", font=FONT_LABEL).grid(row=0, column=4, sticky="w", padx=10, pady=7); self.gioitinh_combo = ttk.Combobox(input_frame, textvariable=self.gioitinh_var, values=['Nam', 'Nữ'], font=FONT_ENTRY, state='readonly'); self.gioitinh_combo.grid(row=0, column=5, padx=10, pady=7, sticky="ew"); self.gioitinh_combo.bind('<<ComboboxSelected>>', self.update_available_rooms)
        
        tk.Label(input_frame, text="Lớp:", font=FONT_LABEL).grid(row=1, column=0, sticky="w", padx=10, pady=7); self.lop_entry = tk.Entry(input_frame, textvariable=self.lop_var, font=FONT_ENTRY); self.lop_entry.grid(row=1, column=1, padx=10, pady=7, sticky="ew")
        tk.Label(input_frame, text="Số điện thoại:", font=FONT_LABEL).grid(row=1, column=2, sticky="w", padx=10, pady=7); self.sdt_entry = tk.Entry(input_frame, textvariable=self.sdt_var, font=FONT_ENTRY); self.sdt_entry.grid(row=1, column=3, padx=10, pady=7, sticky="ew")
        tk.Label(input_frame, text="Ngày sinh:", font=FONT_LABEL).grid(row=1, column=4, sticky="w", padx=10, pady=7); self.ngaysinh_entry = DateEntry(input_frame, textvariable=self.ngaysinh_var, font=FONT_ENTRY, date_pattern='dd/mm/y', selectmode='day', showweeknumbers=False); self.ngaysinh_entry.grid(row=1, column=5, padx=10, pady=7, sticky="ew")
        
        tk.Label(input_frame, text="Quê quán:", font=FONT_LABEL).grid(row=2, column=0, sticky="w", padx=10, pady=7); self.quequan_entry = tk.Entry(input_frame, textvariable=self.quequan_var, font=FONT_ENTRY); self.quequan_entry.grid(row=2, column=1, padx=10, pady=7, sticky="ew")
        tk.Label(input_frame, text="Ngày vào:", font=FONT_LABEL).grid(row=2, column=2, sticky="w", padx=10, pady=7); self.ngayvao_entry = DateEntry(input_frame, textvariable=self.ngayvao_var, font=FONT_ENTRY, date_pattern='dd/mm/y', selectmode='day', showweeknumbers=False); self.ngayvao_entry.grid(row=2, column=3, padx=10, pady=7, sticky="ew")
        tk.Label(input_frame, text="Mã phòng:", font=FONT_LABEL).grid(row=2, column=4, sticky="w", padx=10, pady=7); self.maphong_combo = ttk.Combobox(input_frame, textvariable=self.maphong_var, font=FONT_ENTRY, state='readonly'); self.maphong_combo.grid(row=2, column=5, padx=10, pady=7, sticky="ew")

    # --- Các hàm còn lại (Giữ nguyên) ---
    def create_button_frame(self, parent):
        button_frame = tk.Frame(parent, pady=10); button_frame.pack(fill="x")
        self.btn_them = tk.Button(button_frame, text="Thêm", font=FONT_BUTTON, width=10, bg="#4CAF50", fg="white", command=self.action_add); self.btn_them.pack(side="left", padx=10, pady=5)
        self.btn_luu = tk.Button(button_frame, text="Lưu", font=FONT_BUTTON, width=10, bg="#008CBA", fg="white", command=self.action_save); self.btn_luu.pack(side="left", padx=10, pady=5)
        self.btn_sua = tk.Button(button_frame, text="Sửa", font=FONT_BUTTON, width=10, bg="#f44336", fg="white", command=self.action_edit); self.btn_sua.pack(side="left", padx=10, pady=5)
        self.btn_xoa = tk.Button(button_frame, text="Xóa", font=FONT_BUTTON, width=10, bg="#555555", fg="white", command=self.action_delete); self.btn_xoa.pack(side="left", padx=10, pady=5)
        self.btn_huy = tk.Button(button_frame, text="Hủy", font=FONT_BUTTON, width=10, bg="#ff9800", fg="white", command=self.action_cancel); self.btn_huy.pack(side="left", padx=10, pady=5)
        self.btn_log_payment = tk.Button(button_frame, text="Ghi nhận đóng tiền", font=FONT_BUTTON, width=15, bg="#28a745", fg="white", command=self.open_log_payment_window, state="disabled"); self.btn_log_payment.pack(side="left", padx=10, pady=5)
        self.btn_view_history = tk.Button(button_frame, text="Xem lịch sử", font=FONT_BUTTON, width=12, command=self.open_history_window, state="disabled"); self.btn_view_history.pack(side="left", padx=10, pady=5)
        self.btn_logout = tk.Button(button_frame, text="Đăng xuất", font=FONT_BUTTON, width=10, command=self.action_logout); self.btn_logout.pack(side="right", padx=10, pady=5)
        self.btn_thoat = tk.Button(button_frame, text="Thoát", font=FONT_BUTTON, width=10, command=self.confirm_exit); self.btn_thoat.pack(side="right", padx=10, pady=5)

    def action_logout(self): self.window.destroy(); self.login_form.clear_credentials(); self.login_window.deiconify()
    def confirm_exit(self):
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát?", parent=self.window): self.on_closing()

    def create_search_frame(self, parent):
        search_frame = tk.LabelFrame(parent, text="Tìm kiếm sinh viên", font=FONT_HEADING, padx=15, pady=10); search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="Nhập Mã SV hoặc Tên SV:", font=FONT_LABEL).pack(side="left", padx=(0, 5))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=FONT_ENTRY); search_entry.pack(side="left", padx=5, fill="x", expand=True)
        tk.Label(search_frame, text="Lọc theo phòng:", font=FONT_LABEL).pack(side="left", padx=(10, 5))
        self.search_room_combo = ttk.Combobox(search_frame, textvariable=self.search_room_var, font=FONT_ENTRY, width=15, state='readonly'); self.search_room_combo.pack(side="left", padx=5)
        self.search_room_combo.bind('<<ComboboxSelected>>', self.search_by_room_only)
        search_button = tk.Button(search_frame, text="Tìm kiếm", font=FONT_BUTTON, command=self.search_student_by_name); search_button.pack(side="left", padx=5)
        reset_button = tk.Button(search_frame, text="Hiện tất cả", font=FONT_BUTTON, command=self.load_all_students); reset_button.pack(side="left", padx=5)

    # --- HÀM ĐÃ SỬA: Quay lại 10 cột ---
    def create_treeview_frame(self, parent):
        tree_frame = tk.LabelFrame(parent, text="Danh sách sinh viên", font=FONT_HEADING, padx=10, pady=10); tree_frame.pack(fill="both", expand=True, pady=5)
        style = ttk.Style(); style.configure("Treeview.Heading", font=FONT_TREEVIEW_HEADING); style.configure("Treeview", font=FONT_TREEVIEW_CONTENT, rowheight=25)
        
        # 1. Định nghĩa 10 cột
        columns = ('mssv', 'hoten', 'lop', 'sdt', 'gioitinh', 'ngaysinh', 'ngayvao', 'quequan', 'maphong', 'trangthai')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', style="Treeview")
        
        # 2. Tạo tiêu đề (heading) cho 10 cột
        self.tree.heading('mssv', text='MSSV', command=lambda: self.on_header_click('MSSV'))
        self.tree.heading('hoten', text='Họ Tên', command=lambda: self.on_header_click('HoTen'))
        self.tree.heading('lop', text='Lớp', command=lambda: self.on_header_click('Lop'))
        self.tree.heading('sdt', text='SĐT', command=lambda: self.on_header_click('SDT'))
        self.tree.heading('gioitinh', text='Giới tính', command=lambda: self.on_header_click('GioiTinh'))
        self.tree.heading('ngaysinh', text='Ngày sinh', command=lambda: self.on_header_click('NgaySinh'))
        self.tree.heading('ngayvao', text='Ngày vào', command=lambda: self.on_header_click('NgayVao'))
        self.tree.heading('quequan', text='Quê quán', command=lambda: self.on_header_click('QueQuan'))
        self.tree.heading('maphong', text='Mã Phòng', command=lambda: self.on_header_click('MaPhong'))
        self.tree.heading('trangthai', text='Tiền phòng (tháng này)')
        
        # 3. Định nghĩa chiều rộng (width) cho 10 cột
        self.tree.column('mssv', width=80, anchor="center")
        self.tree.column('hoten', width=180) # Giữ nguyên
        self.tree.column('lop', width=120) # Giữ nguyên
        self.tree.column('sdt', width=100)
        self.tree.column('gioitinh', width=60, anchor="center")
        self.tree.column('ngaysinh', width=100, anchor="center")
        self.tree.column('ngayvao', width=100, anchor="center")
        self.tree.column('quequan', width=120)
        self.tree.column('maphong', width=80, anchor="center")
        self.tree.column('trangthai', width=150, anchor="center")
        
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview); h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set); v_scroll.pack(side="right", fill="y"); h_scroll.pack(side="bottom", fill="x"); self.tree.pack(fill="both", expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def _load_all_rooms_to_search_combo(self):
        conn = self._get_db_connection();
        if not conn: return
        try: cursor = conn.cursor(); cursor.execute("SELECT DISTINCT MaPhong FROM Phong WHERE MaPhong IS NOT NULL ORDER BY MaPhong"); rooms = [row[0] for row in cursor.fetchall()]; self.search_room_combo['values'] = rooms
        except pyodbc.Error as ex: messagebox.showerror("Lỗi CSDL", f"Không thể tải phòng tìm kiếm.\n{ex}")
        finally:
            if conn: conn.close()
            
    def clear_all_fields(self): 
        self.mssv_var.set(""); self.hoten_var.set(""); self.lop_var.set(""); self.sdt_var.set(""); self.gioitinh_var.set(""); self.ngaysinh_var.set(""); self.ngayvao_var.set(""); self.quequan_var.set(""); self.maphong_var.set("")
        self.maphong_combo['values'] = []

    def toggle_button_state(self, state):
        entry_state = 'disabled'; combo_state = 'disabled'; date_state = 'disabled'
        if state == 'init' or state == 'cancel' or state == 'save':
            self.btn_them.config(state="normal"); self.btn_sua.config(state="disabled"); self.btn_xoa.config(state="disabled"); self.btn_luu.config(state="disabled"); self.btn_huy.config(state="disabled")
            self.btn_log_payment.config(state="disabled"); self.btn_view_history.config(state="disabled") 
        elif state == 'add': 
            entry_state = 'normal'; combo_state = 'readonly'; date_state = 'readonly'
            self.btn_them.config(state="disabled"); self.btn_sua.config(state="disabled"); self.btn_xoa.config(state="disabled"); self.btn_luu.config(state="normal"); self.btn_huy.config(state="normal")
            self.btn_log_payment.config(state="disabled"); self.btn_view_history.config(state="disabled")
        elif state == 'edit': 
            entry_state = 'normal'; combo_state = 'readonly'; date_state = 'readonly'
            self.btn_them.config(state="disabled"); self.btn_sua.config(state="disabled"); self.btn_xoa.config(state="disabled"); self.btn_luu.config(state="normal"); self.btn_huy.config(state="normal")
            self.btn_log_payment.config(state="disabled"); self.btn_view_history.config(state="disabled") 
        elif state == 'select': 
            self.btn_them.config(state="normal"); self.btn_sua.config(state="normal"); self.btn_xoa.config(state="normal"); self.btn_luu.config(state="disabled"); self.btn_huy.config(state="disabled")
            self.btn_log_payment.config(state="normal"); self.btn_view_history.config(state="normal") 
        
        self.mssv_entry.config(state=entry_state); self.hoten_entry.config(state=entry_state); self.lop_entry.config(state=entry_state); self.sdt_entry.config(state=entry_state); self.quequan_entry.config(state=entry_state); self.ngaysinh_entry.config(state=date_state); self.ngayvao_entry.config(state=date_state); self.gioitinh_combo.config(state=combo_state); self.maphong_combo.config(state=combo_state)
        
        if state == 'add': self.mssv_entry.config(state='normal')
        elif state == 'edit' or state == 'select' or state == 'init' or state == 'cancel' or state == 'save': self.mssv_entry.config(state='disabled')

    def update_available_rooms(self, event=None):
        selected_gender = self.gioitinh_var.get(); current_room = self.maphong_var.get(); self.maphong_var.set('')
        if not selected_gender: self.maphong_combo['values'] = []; return
        conn = self._get_db_connection();
        if not conn: return
        try: cursor = conn.cursor(); sql = "SELECT DISTINCT P.MaPhong FROM Phong P JOIN ToaNha T ON P.MaToaNha = T.MaToaNha WHERE (P.TrangThai = N'Trống' AND T.TenToaNha LIKE ?) OR P.MaPhong = ? ORDER BY P.MaPhong"; gender_param = f'%({selected_gender})%'; cursor.execute(sql, gender_param, current_room); rooms = [row[0] for row in cursor.fetchall()]; self.maphong_combo['values'] = rooms
        except pyodbc.Error as ex: messagebox.showerror("Lỗi CSDL", f"Không thể tải phòng.\n{ex}")
        finally:
            if conn: conn.close()

    # --- HÀM ĐÃ SỬA: Insert 10 giá trị ---
    def refresh_treeview(self, sql_query, params=None):
        for item in self.tree.get_children(): self.tree.delete(item)
        conn = self._get_db_connection();
        if not conn: return
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        try:
            cursor = conn.cursor()
            base_query_wrapped = f"({sql_query})"
            
            final_sql = f"""
                SELECT 
                    T1.*, 
                    (SELECT COUNT(MaThanhToan) FROM LichSuDongTien LST 
                     WHERE LST.MSSV = T1.MSSV AND LST.ThangDongTien = ? AND LST.NamDongTien = ?) AS DaDongTien
                FROM {base_query_wrapped} AS T1
                ORDER BY T1.{self.sort_column} {self.sort_order}
            """
            
            full_params = [current_month, current_year] + (params if params else []) 
            
            cursor.execute(final_sql, full_params); rows = cursor.fetchall()
            
            for row in rows:
                # Định dạng lại ngày
                ngay_sinh_dmy = row.NgaySinh.strftime('%d/%m/%Y') if row.NgaySinh else ''
                ngay_vao_dmy = row.NgayVao.strftime('%d/%m/%Y') if row.NgayVao else ''
                # Lấy trạng thái
                trang_thai = 'Đã đóng' if row.DaDongTien > 0 else 'Chưa đóng'
                
                # Insert 10 giá trị
                self.tree.insert('', 'end', values=(
                    row.MSSV, row.HoTen, row.Lop, row.SDT, row.GioiTinh, 
                    ngay_sinh_dmy, ngay_vao_dmy, row.QueQuan, row.MaPhong,
                    trang_thai 
                ))
        except pyodbc.Error as ex: 
            messagebox.showerror("Lỗi Truy vấn SQL", f"Không thể tải dữ liệu SV.\nLỗi: {ex}")
        finally:
            if conn: conn.close()

    def load_all_students(self): 
        self.search_var.set(""); self.search_room_var.set("")
        sql = "SELECT * FROM SinhVien" 
        self.refresh_treeview(sql)
    

    def search_student_by_name(self):
        search_term = self.search_var.get().strip()
        if not search_term: 
            # Cập nhật thông báo thiếu thông tin
            messagebox.showwarning("Thiếu thông tin", "Nhập MSSV, Họ tên sinh viên để tìm kiếm.")
            return
            
        self.search_room_var.set("") 
        
        # Câu SQL này (tìm kiếm CONTAINS) đã bao gồm cả MSSV, Họ tên và Tên (nếu Tên là 1 phần của HoTen)
        sql = "SELECT * FROM SinhVien WHERE (MSSV LIKE ? OR HoTen LIKE ?)"
        params = [f'%{search_term}%', f'%{search_term}%']
        
        # --- THÊM MỚI: Kiểm tra sinh viên có tồn tại không ---
        conn = self._get_db_connection()
        if not conn: return
        
        count_sql = "SELECT COUNT(*) FROM SinhVien WHERE (MSSV LIKE ? OR HoTen LIKE ?)"
        try:
            cursor = conn.cursor()
            cursor.execute(count_sql, params)
            result_count = cursor.fetchone()[0]
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi tìm kiếm: {ex}")
            conn.close()
            return
        finally:
            if conn: conn.close()
            
        if result_count == 0:
            # Cập nhật thông báo không tìm thấy
            messagebox.showinfo("Lỗi", f"Không tìm thấy sinh viên nào có MSSV hoặc Họ tên: '{search_term}'")
        # --- KẾT THÚC THÊM MỚI ---
            
        self.refresh_treeview(sql, params)
    

    def search_by_room_only(self, event=None):
        selected_room = self.search_room_var.get()
        if not selected_room: return
        self.search_var.set("") 
        sql = "SELECT * FROM SinhVien WHERE MaPhong = ?"
        params = [selected_room]
        self.refresh_treeview(sql, params)

    # --- HÀM ĐÃ SỬA: Lấy dữ liệu từ CSDL (Giữ nguyên) ---
    def on_tree_select(self, event):
        try:
            selected_item = self.tree.selection()[0]; item_data = self.tree.item(selected_item, 'values')
            mssv = item_data[0] # Lấy MSSV từ cột 0
            
            conn = self._get_db_connection()
            if not conn: return
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM SinhVien WHERE MSSV = ?", mssv)
            sv = cursor.fetchone()
            conn.close()
            
            if sv:
                self.mssv_var.set(sv.MSSV); self.hoten_var.set(sv.HoTen); self.lop_var.set(sv.Lop or ""); self.sdt_var.set(sv.SDT or "")
                self.gioitinh_var.set(sv.GioiTinh)
                self.ngaysinh_var.set(sv.NgaySinh.strftime('%d/%m/%Y') if sv.NgaySinh else "")
                self.ngayvao_var.set(sv.NgayVao.strftime('%d/%m/%Y') if sv.NgayVao else "")
                self.quequan_var.set(sv.QueQuan or ""); self.maphong_var.set(sv.MaPhong or "")
                
                self.update_available_rooms()
                self.maphong_var.set(sv.MaPhong or "") 
                self.toggle_button_state('select')
        except IndexError: 
            pass 

    # --- HÀM ĐÃ SỬA: Lấy MaPhong từ cột 8 ---
    def open_log_payment_window(self):
        try:
            selected_item = self.tree.selection()[0]; item_values = self.tree.item(selected_item, 'values')
            
            mssv = item_values[0]    # Cột 0
            hoten = item_values[1]   # Cột 1
            maphong = item_values[8] # Cột 8 (Mã Phòng)
            
            conn = self._get_db_connection();
            if not conn: return
            cursor = conn.cursor()
            cursor.execute("SELECT Gia, TienDienNuoc FROM Phong WHERE MaPhong = ?", maphong)
            result = cursor.fetchone()
            gia_phong = result.Gia if result else 0.0
            gia_dien_nuoc = result.TienDienNuoc if result else 0.0
            conn.close()
            
            LogPaymentWindow(self.window, mssv, hoten, maphong, gia_phong, gia_dien_nuoc)
        except IndexError:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để ghi nhận.", parent=self.window)
    
    def open_history_window(self):
        try:
            selected_item = self.tree.selection()[0]; item_values = self.tree.item(selected_item, 'values')
            mssv = item_values[0]    # Cột 0
            hoten = item_values[1]   # Cột 1
            PaymentHistoryWindow(self.window, mssv, hoten)
        except IndexError: messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để xem lịch sử.", parent=self.window)

    def _update_room_status(self, ma_phong, cursor):
        if not ma_phong: return
        try:
            cursor.execute("SELECT LoaiPhong FROM Phong WHERE MaPhong = ?", ma_phong); room_info = cursor.fetchone()
            if not room_info: print(f"Cảnh báo: Không tìm thấy phòng {ma_phong}"); return
            max_capacity = 6 if ('6 người' in room_info.LoaiPhong) else 4
            cursor.execute("SELECT COUNT(MSSV) FROM SinhVien WHERE MaPhong = ?", ma_phong); current_occupancy = cursor.fetchone()[0]
            new_status = 'Đầy' if (current_occupancy >= max_capacity) else 'Trống' 
            cursor.execute("UPDATE Phong SET TrangThai = ? WHERE MaPhong = ?", new_status, ma_phong)
        except Exception as e: raise Exception(f"Lỗi cập nhật trạng thái phòng {ma_phong}: {e}")

    def on_header_click(self, col_name):
        if self.sort_column == col_name:
            self.sort_order = "DESC" if self.sort_order == "ASC" else "ASC"
        else:
            self.sort_column = col_name
            self.sort_order = "ASC"
        
        search_term = self.search_var.get()
        search_room = self.search_room_var.get()
        
        if not search_term and not search_room:
            self.load_all_students()
        elif search_term:
            self.search_student_by_name()
        elif search_room:
             self.search_by_room_only()
        else:
            self.load_all_students()

    def action_add(self): self.clear_all_fields(); self.toggle_button_state('add')
    def action_edit(self): self.toggle_button_state('edit')
    def action_cancel(self): self.clear_all_fields(); self.toggle_button_state('cancel')
    
    def action_delete(self):
        mssv = self.mssv_var.get();
        if not mssv: return
        if not messagebox.askyesno("Xác nhận xóa", f"Xóa sinh viên {mssv}?"): return
        conn = self._get_db_connection();
        if not conn: return
        ma_phong_cu = None
        try:
            cursor = conn.cursor(); conn.autocommit = False; cursor.execute("SELECT MaPhong FROM SinhVien WHERE MSSV = ?", mssv); result = cursor.fetchone()
            if result: ma_phong_cu = result.MaPhong
            cursor.execute("DELETE FROM TaiKhoan WHERE TenDangNhap = ?", mssv); cursor.execute("DELETE FROM SinhVien WHERE MSSV = ?", mssv)
            self._update_room_status(ma_phong_cu, cursor); conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa {mssv}."); self.load_all_students(); self.clear_all_fields(); self.toggle_button_state('cancel')
        except Exception as ex: conn.rollback(); messagebox.showerror("Lỗi CSDL", f"Không thể xóa.\n{ex}")
        finally: conn.autocommit = True; conn.close()
        
    # --- HÀM ĐÃ SỬA: Gộp thông báo thiếu thông tin ---
    def action_save(self):
        def dmy_to_iso(dmy_str):
            if not dmy_str: return None
            try: date_obj = datetime.strptime(dmy_str, '%d/%m/%Y'); return date_obj.strftime('%Y-%m-%d')
            except ValueError: messagebox.showerror("Lỗi Định Dạng", f"Ngày '{dmy_str}' không đúng."); return "ERROR"
        
        # Lấy dữ liệu
        mssv = self.mssv_var.get().strip()
        hoten = self.hoten_var.get().strip()
        sdt = self.sdt_var.get().strip()
        ngaysinh_iso = dmy_to_iso(self.ngaysinh_var.get().strip())
        ngayvao_iso = dmy_to_iso(self.ngayvao_var.get().strip())
        ma_phong_moi = self.maphong_var.get().strip() or None
        
        # --- BẮT ĐẦU KIỂM TRA RÀNG BUỘC ---
        
        if not mssv or not hoten or not ngayvao_iso:
            messagebox.showwarning("Thiếu thông tin", "Bạn phải điền đầy đủ MSSV, Họ tên và Ngày vào.")
            return
            
        # --- SỬA Ở ĐÂY: Thêm kiểm tra phòng ---
        if not ma_phong_moi:
            messagebox.showwarning("Thiếu thông tin", "Bạn phải chọn phòng cho sinh viên.")
            return
        # --- KẾT THÚC SỬA ---
            
        if ngaysinh_iso == "ERROR" or ngayvao_iso == "ERROR": 
             return

        is_add_mode = (self.mssv_entry.cget('state') == 'normal')
        if is_add_mode:
            if not re.match(r'^SV\d{3}$', mssv):
                messagebox.showwarning("Lỗi Mã SV", "Mã số sinh viên không hợp lệ.\nPhải theo định dạng 'SV' và 3 chữ số (ví dụ: SV001, SV123).")
                return

        if sdt: 
            if not re.match(r'^0\d{9}$', sdt):
                messagebox.showwarning("Lỗi Số điện thoại", "Số điện thoại không hợp lệ.\n(Phải bắt đầu bằng '0' và có đúng 10 chữ số).")
                return
        
        # --- KẾT THÚC KIỂM TRA RÀNG BUỘC ---

        ma_phong_cu = None
        conn = self._get_db_connection();
        if not conn: return
        try:
            cursor = conn.cursor(); conn.autocommit = False
            
            if is_add_mode:
                sql_insert_sv = "INSERT INTO SinhVien (MSSV, HoTen, Lop, SDT, GioiTinh, NgaySinh, NgayVao, QueQuan, MaPhong) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                params_sv = (mssv, hoten, self.lop_var.get() or None, sdt or None, self.gioitinh_var.get() or None, ngaysinh_iso, ngayvao_iso, self.quequan_var.get() or None, ma_phong_moi)
                cursor.execute(sql_insert_sv, params_sv); default_pass = mssv[-3:] if len(mssv) >= 3 else '123'
                sql_insert_tk = "INSERT INTO TaiKhoan (TenDangNhap, MatKhau, ChucVu) VALUES (?, ?, N'Sinh viên')"; cursor.execute(sql_insert_tk, mssv, default_pass)
                self._update_room_status(ma_phong_moi, cursor); msg = f"Đã thêm mới {mssv}."
            else:
                cursor.execute("SELECT MaPhong FROM SinhVien WHERE MSSV = ?", mssv); result = cursor.fetchone()
                if result: ma_phong_cu = result.MaPhong
                sql_update_sv = "UPDATE SinhVien SET HoTen=?, Lop=?, SDT=?, GioiTinh=?, NgaySinh=?, NgayVao=?, QueQuan=?, MaPhong=? WHERE MSSV=?" 
                params_sv = (hoten, self.lop_var.get() or None, sdt or None, self.gioitinh_var.get() or None, ngaysinh_iso, ngayvao_iso, self.quequan_var.get() or None, ma_phong_moi, mssv) 
                cursor.execute(sql_update_sv, params_sv)
                if ma_phong_cu != ma_phong_moi: self._update_room_status(ma_phong_cu, cursor); self._update_room_status(ma_phong_moi, cursor)
                msg = f"Đã cập nhật {mssv}."
                
            conn.commit(); messagebox.showinfo("Thành công", msg); self.load_all_students(); self.clear_all_fields(); self.toggle_button_state('save')
        except Exception as ex:
            conn.rollback()
            if "PRIMARY KEY" in str(ex): messagebox.showerror("Lỗi Trùng lặp", f"MSSV '{mssv}' đã tồn tại.")
            else: messagebox.showerror("Lỗi CSDL", f"Không thể lưu.\nChi tiết: {ex}")
        finally: conn.autocommit = True; conn.close()

            