import pyodbc

# --- ⚠️ THÔNG TIN KẾT NỐI SQL SERVER CỦA BẠN ⚠️ ---
SERVER_NAME = 'ADMIN-PC\SQLEXPRESS' # Ví dụ: LAPTOP-ABCD\SQLEXPRESS
DATABASE_NAME = 'QL_KyTucXa01'                   # Tên CSDL của bạn

# Chuỗi kết nối sử dụng Windows Authentication (dùng driver 17 phổ biến)
CONNECTION_STRING = (
    f'DRIVER={{ODBC Driver 11 for SQL Server}};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    'Trusted_Connection=yes;' 
)

def check_credentials_in_sqlserver(username, password):
    """
    Kết nối SQL Server để kiểm tra tài khoản (TenDangNhap) và mật khẩu (MatKhau).
    Trả về ChucVu (Quản lý/Sinh viên) nếu thành công, ngược lại trả về None.
    """
    conn = None
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        
        # Truy vấn kiểm tra TenDangNhap và MatKhau
        sql_query = "SELECT ChucVu FROM TaiKhoan WHERE TenDangNhap=? AND MatKhau=?"
        cursor.execute(sql_query, (username, password))
        
        result = cursor.fetchone()
        
        if result:
            return result[0].strip() # Trả về ChucVu
        else:
            return None

    except pyodbc.Error as ex:
        # Ghi lỗi kết nối ra console để debug
        print(f"❌ LỖI KẾT NỐI/TRUY VẤN SQL SERVER: {ex}") 
        return "ERROR_DB_CONNECTION" 
    finally:
        if conn:
            conn.close()
            