# DoAn_Python.NhomDoAn15.DH24TH1_01_01
---
# 🏫 ỨNG DỤNG QUẢN LÝ KÝ TÚC XÁ  
📘 *Đồ án môn Lập trình Python (COS525)*  

---

## 🧩 Giới thiệu  
Đây là **Ứng dụng quản lý ký túc xá sinh viên** được phát triển trong khuôn khổ **Môn Lập trình Python** tại **Trường Đại học An Giang – Khoa Công nghệ Thông tin**.  
Ứng dụng được xây dựng bằng **Python**, sử dụng **Tkinter** để thiết kế giao diện và **MySQL** để quản lý dữ liệu.  

Cho phép nhân viên quản lý thực hiện các chức năng cơ bản như:
- Thêm, sửa, xóa và lưu thông tin sinh viên ở ký túc xá  
- Quản lý phòng, quản lý sinh viên 
- Tra cứu và thống kê danh sách sinh viên  
- Giao diện thân thiện, trực quan, dễ sử dụng  

---

## ⚙️ Công nghệ sử dụng
| Thành phần | Mô tả |
|-------------|-------|
| 🐍 **Python** | Ngôn ngữ lập trình chính |
| 🪟 **Tkinter** | Tạo giao diện người dùng (GUI) |
| 🗄️ **SQL Server** | Lưu trữ và quản lý dữ liệu ký túc xá |
| 🔗 **pyodbc** | Thư viện giúp Python kết nối với SQL Server |
| 📅 **tkcalendar** | Hỗ trợ chọn ngày sinh, ngày vào ký túc xá |

---

## 🎯 Chức năng chính
- 👤 **Quản lý sinh viên:**  
  - Thêm / sửa / xóa sinh viên  
  - Lưu thông tin và hiển thị danh sách  
  - Tìm kiếm theo mã sinh viên, họ tên, phòng ở  

- 🏠 **Quản lý phòng ký túc:**  
  - Hiển thị danh sách phòng  
  - Theo dõi số lượng sinh viên trong phòng  
  - Cập nhật tình trạng phòng (trống / đầy)

- 💰 **Quản lý chi phí:**  
  - Theo dõi tiền phòng, tiền điện nước theo tháng  
  - Thống kê tổng chi phí theo sinh viên 

- 📊 **Thống kê & báo cáo:**  
  - Xuất danh sách sinh viên theo phòng
  - Thống kê phòng đang trống, phòng đầy  

---

## 🗄️ Cấu trúc cơ sở dữ liệu
Cơ sở dữ liệu SQL Server gồm các bảng chính:

### 🏢 **Bảng ToaNha**
| Tên cột | Kiểu dữ liệu | Ghi chú |
|----------|---------------|---------|
| MaToaNha | VARCHAR(10) | 🔑 Khóa chính |
| TenToaNha | NVARCHAR(50) | Tên tòa nhà (ví dụ: “Tòa A (Nam)”) |

---

### 👩‍💼 **Bảng QuanLy**
| Tên cột | Kiểu dữ liệu | Ghi chú |
|----------|---------------|---------|
| MaQuanLy | VARCHAR(10) | 🔑 Khóa chính |
| HoTenQuanLy | NVARCHAR(100) | Họ tên quản lý |
| MaToaQuanLy | VARCHAR(10) | 🔗 Khóa ngoại → `ToaNha(MaToaNha)` |

---

### 🏠 **Bảng Phong**
| Tên cột | Kiểu dữ liệu | Ghi chú |
|----------|---------------|---------|
| MaPhong | VARCHAR(10) | 🔑 Khóa chính |
| LoaiPhong | NVARCHAR(50) | Loại phòng (4 người / 6 người) |
| Gia | DECIMAL(10,2) | Giá phòng mỗi tháng |
| TrangThai | NVARCHAR(20) | “Đầy” hoặc “Trống” |
| MaToaNha | VARCHAR(10) | 🔗 Khóa ngoại → `ToaNha(MaToaNha)` |

---

### 🎓 **Bảng SinhVien**
| Tên cột | Kiểu dữ liệu | Ghi chú |
|----------|---------------|---------|
| MSSV | VARCHAR(20) | 🔑 Khóa chính |
| HoTen | NVARCHAR(100) | Họ và tên sinh viên |
| Lop | NVARCHAR(50) | Lớp học |
| SDT | VARCHAR(15) | Số điện thoại |
| GioiTinh | NVARCHAR(5) | “Nam” hoặc “Nữ” |
| NgaySinh | DATE | Ngày sinh |
| NgayVao | DATE | Ngày vào ký túc |
| QueQuan | NVARCHAR(100) | Quê quán |
| MaPhong | VARCHAR(10) | 🔗 Khóa ngoại → `Phong(MaPhong)` |

---

### 🔐 **Bảng TaiKhoan**
| Tên cột | Kiểu dữ liệu | Ghi chú |
|----------|---------------|---------|
| UserID | INT (IDENTITY) | 🔑 Khóa chính |
| TenDangNhap | VARCHAR(50) | Tên đăng nhập (MSSV hoặc Mã quản lý) |
| MatKhau | VARCHAR(255) | Mật khẩu (3 ký tự cuối của mã) |
| ChucVu | NVARCHAR(20) | “Sinh viên” hoặc “Quản lý” |

---

## 🚀 Cách cài đặt & chạy chương trình

### 1️⃣ Cài đặt môi trường  
**Yêu cầu:**  
- 🐍 **Python:** Đảm bảo bạn đã cài đặt Python trên máy tính của mình.
- 🧩 **SQL Server:** Cài đặt **Microsoft SQL Server** và tạo cơ sở dữ liệu `QL_KyTucXa`.  
- 🔗 **ODBC Driver:** Cài đặt **ODBC Driver 17 for SQL Server** (hoặc bản mới hơn) để Python có thể kết nối với SQL Server.  
- 📦 **Các thư viện Python cần thiết:**  
### 2️⃣ Tạo cơ sở dữ liệu MySQL
### 3️⃣ Viết mã Python kết nối MySQL  
### 4️⃣ Chạy chương trình

---

## 👨‍💻 Nhóm thực hiện đồ án
| Họ tên         | Mã số SV  |
|----------------|-----------|
| Phạm Thanh Tân | DTH235761 | 
| Vũ Thị Yến Vy  | DTH235820 | 
---

## 🏁 Kết luận
Dự án Ứng dụng quản lý ký túc xá giúp sinh viên vận dụng kiến thức **Python, Tkinter, SQL Server** để xây dựng ứng dụng thực tế phục vụ công tác quản lý ký túc xá một cách hiệu quả và chính xác.  

## 📜 Giấy phép
Dự án phục vụ mục đích **học tập** trong môn *Lập trình Python – Đại học An Giang*.  
Không sử dụng cho mục đích thương mại. 

## 📬 Liên hệ
Nếu bạn có bất kỳ thắc mắc hoặc góp ý nào về dự án, vui lòng liên hệ với các thành viên của nhóm thực hiện qua email:

📧 Phạm Thanh Tân – tan_dth234761@student.agu.edu.vn
📧 Vũ Thị Yến Vy – vy_dth235820@student.agu.edu.vn


