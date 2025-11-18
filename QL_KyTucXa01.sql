-- 1. Tạo Database
-- Thay thế 'QL_KyTucXa' bằng tên bạn muốn nếu cần

CREATE DATABASE QL_KyTucXa01;
GO

USE QL_KyTucXa01; -- Thay thế QL_KyTucXa bằng tên Database của bạn nếu cần thiết 
GO

IF OBJECT_ID('SinhVien', 'U') IS NOT NULL DROP TABLE SinhVien;
GO
IF OBJECT_ID('TaiKhoan', 'U') IS NOT NULL DROP TABLE TaiKhoan;
GO
IF OBJECT_ID('Phong', 'U') IS NOT NULL DROP TABLE Phong;
GO
IF OBJECT_ID('QuanLy', 'U') IS NOT NULL DROP TABLE QuanLy;
GO
IF OBJECT_ID('ToaNha', 'U') IS NOT NULL DROP TABLE ToaNha;
GO
----------------------------------------------------
-- 1. BẢNG TÒA NHÀ (Cha của Bảng Phòng)
----------------------------------------------------
IF OBJECT_ID('ToaNha', 'U') IS NOT NULL DROP TABLE ToaNha;
GO

CREATE TABLE ToaNha (
    MaToaNha VARCHAR(10) PRIMARY KEY, -- PK
    TenToaNha NVARCHAR(50) NOT NULL UNIQUE
);
GO

-- Dữ liệu mẫu
INSERT INTO ToaNha (MaToaNha, TenToaNha) VALUES 
    ('A', N'Tòa nhà A (Nam)'),
    ('B', N'Tòa nhà B (Nữ)'),
	('C', N'Tòa nhà C (Nam)'),
	('D', N'Tòa nhà D (Nữ)');

GO

----------------------------------------------------
-- 2. BẢNG QUẢN LÝ (Liên kết với Bảng Tòa nhà)
----------------------------------------------------
IF OBJECT_ID('QuanLy', 'U') IS NOT NULL DROP TABLE QuanLy;
GO

CREATE TABLE QuanLy (
    MaQuanLy VARCHAR(10) PRIMARY KEY, -- PK
    HoTenQuanLy NVARCHAR(100) NOT NULL,
    MaToaQuanLy VARCHAR(10) NOT NULL, -- FK
    
    -- Khóa ngoại liên kết Quản lý với Tòa nhà
    FOREIGN KEY (MaToaQuanLy) REFERENCES ToaNha(MaToaNha)
        ON UPDATE CASCADE 
        ON DELETE NO ACTION -- Không cho xóa Tòa nhà nếu còn Quản lý
);
GO

-- Dữ liệu mẫu
INSERT INTO QuanLy (MaQuanLy, HoTenQuanLy, MaToaQuanLy) VALUES
    ('QL001', N'Trần Thị Mai', 'A'),
    ('QL002', N'Lê Văn Phát', 'B'),
	('QL003', N'Phan Thị Thanh Tiền', 'C'),
	('QL004', N'Lâm Đức Trường', 'D');

GO

----------------------------------------------------
-- 3. BẢNG PHÒNG (Liên kết với Bảng Tòa nhà)
----------------------------------------------------
IF OBJECT_ID('Phong', 'U') IS NOT NULL DROP TABLE Phong;
GO


CREATE TABLE Phong (
    MaPhong VARCHAR(10) PRIMARY KEY, -- PK
    LoaiPhong NVARCHAR(50) NOT NULL 
        CHECK (LoaiPhong IN (N'4 người', N'6 người')),
    Gia DECIMAL(10, 2) NOT NULL,
    TrangThai NVARCHAR(20) NOT NULL 
        CHECK (TrangThai IN (N'Đầy', N'Trống')),
    MaToaNha VARCHAR(10) NOT NULL, -- FK
    
    -- Khóa ngoại liên kết Phòng với Tòa nhà
    FOREIGN KEY (MaToaNha) REFERENCES ToaNha(MaToaNha)
        ON UPDATE CASCADE 
        ON DELETE CASCADE -- Nếu Tòa nhà bị xóa, các Phòng thuộc Tòa đó cũng bị xóa
);
GO
ALTER TABLE Phong
ADD TienDienNuoc DECIMAL(10, 2);
GO
-- Cập nhật giá điện nước cho tất cả 'Phòng 4 người'
UPDATE Phong
SET TienDienNuoc = 70000.00
WHERE LoaiPhong = N'4 người';
GO

-- Cập nhật giá điện nước cho tất cả 'Phòng 6 người'
UPDATE Phong
SET TienDienNuoc = 100000.00
WHERE LoaiPhong = N'6 người';
GO

-- 4. (Tùy chọn) Kiểm tra lại kết quả để xem
SELECT MaPhong, LoaiPhong, Gia, TienDienNuoc
FROM Phong;
GO

DELETE FROM SinhVien;
GO
-- Dữ liệu mẫu
INSERT INTO Phong (MaPhong, LoaiPhong, Gia, TrangThai, MaToaNha) VALUES 
    ('A101', N'4 người', 600000.00, N'Đầy', 'A'),
    ('A102', N'4 người', 600000.00, N'Đầy', 'A'),
    ('A103', N'4 người', 600000.00, N'Đầy', 'A'),
    ('A104', N'4 người', 600000.00, N'Đầy', 'A'),
    ('A105', N'4 người', 600000.00, N'Đầy', 'A'),
    -- 5 phòng 6 người
    ('A206', N'6 người', 400000.00, N'Đầy', 'A'),
    ('A207', N'6 người', 400000.00, N'Trống', 'A'),
    ('A208', N'6 người', 400000.00, N'Trống', 'A'),
    ('A209', N'6 người', 400000.00, N'Trống', 'A'),
    ('A210', N'6 người', 400000.00, N'Trống', 'A'),

-- TÒA NHÀ B (10 PHÒNG)
    -- 5 phòng 4 người
    ('B101', N'4 người', 600000.00, N'Đầy', 'B'),
    ('B102', N'4 người', 600000.00, N'Đầy', 'B'),
    ('B103', N'4 người', 600000.00, N'Đầy', 'B'),
    ('B104', N'4 người', 600000.00, N'Đầy', 'B'),
    ('B105', N'4 người', 600000.00, N'Đầy', 'B'),
    -- 5 phòng 6 người (Giá cao hơn cho mục đích kiểm thử)
    ('B206', N'6 người', 400000.00, N'Đầy', 'B'), 
    ('B207', N'6 người', 400000.00, N'Trống', 'B'),
    ('B208', N'6 người', 400000.00, N'Trống', 'B'),
    ('B209', N'6 người', 400000.00, N'Trống', 'B'),
    ('B210', N'6 người', 400000.00, N'Trống', 'B'),

-- TÒA NHÀ C (10 PHÒNG)
    ('C101', N'4 người', 600000.00, N'Đầy', 'C'), ('C206', N'6 người', 400000.00, N'Trống', 'C'),
    ('C102', N'4 người', 600000.00, N'Đầy', 'C'), ('C207', N'6 người', 400000.00, N'Trống', 'C'),
    ('C103', N'4 người', 600000.00, N'Đầy', 'C'), ('C208', N'6 người', 400000.00, N'Trống', 'C'),
    ('C104', N'4 người', 600000.00, N'Đầy', 'C'), ('C209', N'6 người', 400000.00, N'Trống', 'C'),
    ('C105', N'4 người', 600000.00, N'Trống', 'C'), ('C210', N'6 người',400000.00, N'Trống', 'C'),

-- TÒA NHÀ D (10 PHÒNG)
    ('D101', N'4 người', 600000.00, N'Đầy', 'D'), ('D206', N'6 người', 400000.00, N'Trống', 'D'),
    ('D102', N'4 người', 600000.00, N'Đầy', 'D'), ('D207', N'6 người', 400000.00, N'Trống', 'D'),
    ('D103', N'4 người', 600000.00, N'Đầy', 'D'), ('D208', N'6 người', 400000.00, N'Trống', 'D'),
    ('D104', N'4 người', 600000.00, N'Đầy', 'D'), ('D209', N'6 người', 400000.00, N'Trống', 'D'),
    ('D105', N'4 người', 600000.00, N'Trống', 'D'), ('D210', N'6 người', 400000.00, N'Trống', 'D');
GO




----------------------------------------------------
-- 4. BẢNG SINH VIÊN (Liên kết với Bảng Phòng)
----------------------------------------------------
IF OBJECT_ID('SinhVien', 'U') IS NOT NULL DROP TABLE SinhVien;
GO

CREATE TABLE SinhVien (
    MSSV VARCHAR(20) PRIMARY KEY, -- PK (Mã số sinh viên)
    HoTen NVARCHAR(100) NOT NULL,
    Lop NVARCHAR(50),
    SDT VARCHAR(15),
    GioiTinh NVARCHAR(5) DEFAULT N'Nam', -- Mặc định là Nam
	NgaySinh DATE,
    NgayVao DATE NOT NULL,
    QueQuan NVARCHAR(100),
    MaPhong VARCHAR(10), -- FK
    
    -- Khóa ngoại liên kết Sinh viên với Phòng
    FOREIGN KEY (MaPhong) REFERENCES Phong(MaPhong)
        ON UPDATE CASCADE 
        ON DELETE SET NULL -- Khi Phòng bị xóa, MaPhong của Sinh viên được đặt là NULL
);
GO
ALTER TABLE SinhVien
ADD TrangThaiTienPhong NVARCHAR(20) DEFAULT N'Chưa đóng'; -- Mặc định là 'Chưa đóng'
GO

-- Dữ liệu mẫu
INSERT INTO SinhVien (MSSV, HoTen, Lop, SDT, MaPhong, GioiTinh, NgaySinh, NgayVao, QueQuan) VALUES 
-- NAM - TÒA A
-- A101 (4 SV)
('SV001', N'Nguyễn Văn Anh', N'Marketing', '0901234567', 'A101', N'Nam', '2005-12-02', '2025-09-01', N'Hà Nội'),
('SV003', N'Ngô Văn Cao', N'Marketing', '0913174143', 'A101', N'Nam', '2006-10-15', '2025-03-08', N'An Giang'),
('SV005', N'Lê Thanh Trí', N'CNTT', '0949055708', 'A101', N'Nam', '2003-02-02', '2023-10-09', N'Bến Tre'),
('SV006', N'Võ Thành Nhân', N'CNTT', '0375616199', 'A101', N'Nam', '2007-04-02', '2025-11-01', N'Đồng Tháp'),
-- A102 (4 SV)
('SV007', N'Phạm Minh Hoàng', N'CNTT', '0912345678', 'A102', N'Nam', '2005-07-12', '2025-09-15', N'Hải Phòng'),
('SV009', N'Lê Văn Khánh', N'Trí tuệ nhân tạo', '0976543210', 'A102', N'Nam', '2006-05-18', '2025-03-30', N'Quảng Ninh'),
('SV011', N'Đỗ Quốc Bảo', N'Luật', '0911222333', 'A102', N'Nam', '2005-01-25', '2025-10-12', N'Nam Định'),
('SV013', N'Nguyễn Văn Phúc', N'Y khoa', '0988776655', 'A102', N'Nam', '2006-12-01', '2025-12-01', N'Thừa Thiên Huế'),
-- A103 (4 SV)
('SV015', N'Nguyễn Văn Hùng', N'CNTT', '0912345001', 'A103', N'Nam', '2005-01-12', '2025-09-10', N'Hà Nội'),
('SV017', N'Lê Văn Phước', N'Kỹ thuật phần mềm', '0912345003', 'A103', N'Nam', '2006-07-18', '2025-03-20', N'Đà Nẵng'),
('SV019', N'Hoàng Văn Minh', N'Trí tuệ nhân tạo', '0912345005', 'A103', N'Nam', '2005-05-25', '2025-11-01', N'Nam Định'),
('SV021', N'Đỗ Văn Quang', N'Luật', '0912345007', 'A103', N'Nam', '2006-02-01', '2025-12-01', N'Thừa Thiên Huế'),
-- A104 (4 SV)
('SV023', N'Phan Văn Khải', N'Logistics', '0912345009', 'A104', N'Nam', '2005-08-30', '2025-09-15', N'Quảng Ninh'),
('SV025', N'Ngô Văn Dũng', N'Y khoa', '0912345011', 'A104', N'Nam', '2006-04-05', '2025-03-30', N'Bình Định'),
('SV027', N'Nguyễn Văn Toàn', N'Quản trị kinh doanh', '0912345013', 'A104', N'Nam', '2005-02-14', '2025-10-12', N'Cần Thơ'),
('SV029', N'Hoàng Văn Tùng', N'CNTT', '0912345015', 'A104', N'Nam', '2006-01-25', '2025-12-01', N'An Giang'),
-- A105 (4 SV)
('SV031', N'Đặng Văn Lâm', N'Kỹ thuật phần mềm', '0912345017', 'A105', N'Nam', '2005-09-09', '2025-09-20', N'Long An'),
('SV033', N'Lê Văn Hòa', N'Trí tuệ nhân tạo', '0912345019', 'A105', N'Nam', '2006-06-18', '2025-03-30', N'Quảng Bình'),
('SV035', N'Nguyễn Văn Khánh', N'CNTT', '0912345021', 'A105', N'Nam', '2005-04-12', '2025-09-10', N'Hà Giang'),
('SV037', N'Lê Văn Hậu', N'Kỹ thuật phần mềm', '0912345023', 'A105', N'Nam', '2006-07-18', '2025-03-20', N'Quảng Nam'),
-- A206 (6 SV)
('SV071', N'Ngô Văn Thắng', N'Y khoa', '0912345057', 'A206', N'Nam', '2005-04-05', '2025-03-30', N'Đắk Nông'),
('SV073', N'Nguyễn Văn Nam', N'Khoa học dữ liệu', '0912345059', 'A206', N'Nam', '2006-02-14', '2025-10-12', N'Tây Ninh'),
('SV075', N'Hoàng Văn Tùng', N'Quản trị kinh doanh', '0912345061', 'A206', N'Nam', '2005-01-25', '2025-12-01', N'Vĩnh Long'),
('SV077', N'Đặng Văn Lâm', N'CNTT', '0912345063', 'A206', N'Nam', '2006-09-09', '2025-09-20', N'An Giang'),
('SV079', N'Lê Văn Hòa', N'Trí tuệ nhân tạo', '0912345065', 'A206', N'Nam', '2005-06-18', '2025-03-30', N'Quảng Trị'),
('SV081', N'Nguyễn Văn Hòa', N'Kỹ thuật phần mềm', '0912345067', 'A206', N'Nam', '2006-04-12', '2025-09-10', N'Lạng Sơn'),
-- NAM - TÒA C
-- C101 (4 SV)
('SV039', N'Hoàng Văn Duy', N'Trí tuệ nhân tạo', '0912345025', 'C101', N'Nam', '2005-05-25', '2025-11-01', N'Thái Bình'),
('SV041', N'Đỗ Văn Hùng', N'Luật', '0912345027', 'C101', N'Nam', '2006-02-01', '2025-12-01', N'Bình Phước'),
('SV043', N'Phan Văn Lợi', N'Logistics', '0912345029', 'C101', N'Nam', '2005-08-30', '2025-09-15', N'Quảng Trị'),
('SV045', N'Ngô Văn Hòa', N'Y khoa', '0912345031', 'C101', N'Nam', '2006-04-05', '2025-03-30', N'Bình Thuận'),
-- C102 (4 SV)
('SV047', N'Nguyễn Văn Hưng', N'Quản trị kinh doanh', '0912345033', 'C102', N'Nam', '2005-02-14', '2025-10-12', N'Trà Vinh'),
('SV049', N'Hoàng Văn Quân', N'CNTT', '0912345035', 'C102', N'Nam', '2006-01-25', '2025-12-01', N'Bạc Liêu'),
('SV051', N'Đặng Văn Hòa', N'Kỹ thuật phần mềm', '0912345037', 'C102', N'Nam', '2005-09-09', '2025-09-20', N'Lào Cai'),
('SV053', N'Lê Văn Hùng', N'Trí tuệ nhân tạo', '0912345039', 'C102', N'Nam', '2006-06-18', '2025-03-30', N'Yên Bái'),
-- C103 (4 SV)
('SV055', N'Nguyễn Văn Hòa', N'Luật', '0912345041', 'C103', N'Nam', '2005-04-12', '2025-09-10', N'Hà Tĩnh'),
('SV057', N'Lê Văn Hưng', N'Logistics', '0912345043', 'C103', N'Nam', '2006-07-18', '2025-03-20', N'Gia Lai'),
('SV059', N'Hoàng Văn Hùng', N'Y khoa', '0912345045', 'C103', N'Nam', '2005-05-25', '2025-11-01', N'Điện Biên'),
('SV061', N'Đặng Văn Phú', N'Quản trị kinh doanh', '0912345047', 'C103', N'Nam', '2006-01-12', '2025-09-10', N'Bình Dương'),
-- C104 (4 SV)
('SV063', N'Lê Văn Long', N'CNTT', '0912345049', 'C104', N'Nam', '2005-07-18', '2025-03-20', N'Đồng Nai'),
('SV065', N'Hoàng Văn Sơn', N'Kỹ thuật phần mềm', '0912345051', 'C104', N'Nam', '2006-05-25', '2025-11-01', N'Bắc Kạn'),
('SV067', N'Đỗ Văn Tài', N'Trí tuệ nhân tạo', '0912345053', 'C104', N'Nam', '2005-02-01', '2025-12-01', N'Hưng Yên'),
('SV069', N'Phan Văn Lâm', N'Logistics', '0912345055', 'C104', N'Nam', '2006-08-30', '2025-09-15', N'Bình Định'),
-- NỮ - TÒA B 
-- B101 (4 SV)
('SV002', N'Trần Thị Bích', N'Marketing', '0919876543', 'B101', N'Nữ', '2004-03-02', '2024-12-09', N'TP. Hồ Chí Minh'),
('SV004', N'Lê Thanh Trúc', N'CNTT', '0947060710', 'B101', N'Nữ', '2005-11-07', '2023-10-01', N'Cần Thơ'),
('SV008', N'Nguyễn Thị Mai', N'Marketing', '0938765432', 'B101', N'Nữ', '2004-11-23', '2024-12-20', N'Đà Nẵng'),
('SV010', N'Trần Thị Hồng Nhung', N'Ngôn ngữ Anh', '0909988776', 'B101', N'Nữ', '2003-09-09', '2023-11-05', N'Khánh Hòa'),
-- B102 (4 SV)
('SV012', N'Vũ Thị Lan', N'Tài chính - Ngân hàng', '0963344556', 'B102', N'Nữ', '2004-06-14', '2024-09-28', N'Nghệ An'),
('SV014', N'Hoàng Thị Thu Trang', N'Du lịch', '0922233444', 'B102', N'Nữ', '2003-03-19', '2023-10-15', N'Lâm Đồng'),
('SV016', N'Trần Thị Thu Hà', N'Marketing', '0912345002', 'B102', N'Nữ', '2004-03-22', '2024-12-05', N'Hải Phòng'),
('SV018', N'Phạm Thị Hồng', N'Ngôn ngữ Anh', '0912345004', 'B102', N'Nữ', '2003-11-09', '2023-10-15', N'TP. Hồ Chí Minh'),
-- B103 (4 SV)
('SV020', N'Vũ Thị Lan Anh', N'Du lịch', '0912345006', 'B103', N'Nữ', '2004-09-14', '2024-09-28', N'Nghệ An'),
('SV022', N'Nguyễn Thị Mai', N'Tài chính - Ngân hàng', '0912345008', 'B103', N'Nữ', '2003-06-19', '2023-11-20', N'Lâm Đồng'),
('SV024', N'Lê Thị Bích Ngọc', N'Kinh tế', '0912345010', 'B103', N'Nữ', '2004-12-12', '2024-12-10', N'Khánh Hòa'),
('SV026', N'Phạm Thị Hương', N'Công nghệ sinh học', '0912345012', 'B103', N'Nữ', '2003-10-21', '2023-10-25', N'Bến Tre'),
-- B104 (4 SV)
('SV028', N'Trần Thị Thanh', N'Khoa học dữ liệu', '0912345014', 'B104', N'Nữ', '2004-07-07', '2024-09-28', N'Đồng Nai'),
('SV030', N'Vũ Thị Hồng Nhung', N'Marketing', '0912345016', 'B104', N'Nữ', '2003-05-19', '2023-11-05', N'Kiên Giang'),
('SV032', N'Nguyễn Thị Thu', N'Ngôn ngữ Anh', '0912345018', 'B104', N'Nữ', '2004-11-23', '2024-12-20', N'Bắc Giang'),
('SV034', N'Phạm Thị Yến', N'Du lịch', '0912345020', 'B104', N'Nữ', '2003-08-09', '2023-10-15', N'Tuyên Quang'),
-- B105 (4 SV)
('SV036', N'Trần Thị Hồng', N'Marketing', '0912345022', 'B105', N'Nữ', '2004-08-22', '2024-12-05', N'Bắc Ninh'),
('SV038', N'Phạm Thị Thu', N'Ngôn ngữ Anh', '0912345024', 'B105', N'Nữ', '2003-11-09', '2023-10-15', N'TP. Hồ Chí Minh'),
('SV040', N'Vũ Thị Hạnh', N'Du lịch', '0912345026', 'B105', N'Nữ', '2004-09-14', '2024-09-28', N'Đắk Lắk'),
('SV042', N'Nguyễn Thị Hòa', N'Tài chính - Ngân hàng', '0912345028', 'B105', N'Nữ', '2003-06-19', '2023-11-20', N'Kon Tum'),
-- B206 (6 SV)
('SV076', N'Vũ Thị Hồng Nhung', N'Marketing', '0912345062', 'B206', N'Nữ', '2004-05-19', '2024-11-05', N'Bạc Liêu'),
('SV078', N'Nguyễn Thị Thu', N'Du lịch', '0912345064', 'B206', N'Nữ', '2003-11-23', '2023-12-20', N'Cà Mau'),
('SV080', N'Phạm Thị Yến', N'Luật', '0912345066', 'B206', N'Nữ', '2004-08-09', '2024-10-15', N'Hòa Bình'),
('SV082', N'Trần Thị Hồng Nhung', N'Tài chính - Ngân hàng', '0912345068', 'B206', N'Nữ', '2003-08-22', '2023-12-05', N'Tuyên Quang'),
('SV083', N'Lê Ngọc Hân', N'Logistics', '0912345069', 'B206', N'Nữ', '2005-07-18', '2025-03-20', N'Điện Biên'), 
('SV084', N'Phạm Thị Thu Trang', N'Ngôn ngữ Anh', '0912345070', 'B206', N'Nữ', '2004-11-09', '2024-12-15', N'Sơn La'),
-- NỮ - TÒA D
-- D101 (4 SV)
('SV044', N'Lê Thị Ngọc', N'Kinh tế', '0912345030', 'D101', N'Nữ', '2004-12-12', '2024-12-10', N'Phú Yên'),
('SV046', N'Phạm Thị Thảo', N'Công nghệ sinh học', '0912345032', 'D101', N'Nữ', '2003-10-21', '2023-10-25', N'Sóc Trăng'),
('SV048', N'Vũ Thị Yến Vy', N'CNTT', '0912345034', 'D101', N'Nữ', '2005-11-09', '2024-09-28', N'An Giang'),
('SV050', N'Vũ Thị Hồng', N'Marketing', '0912345036', 'D101', N'Nữ', '2003-05-19', '2023-11-05', N'Cao Bằng'),
-- D102 (4 SV)
('SV052', N'Nguyễn Thị Thu Hằng', N'Ngôn ngữ Anh', '0912345038', 'D102', N'Nữ', '2004-11-23', '2024-12-20', N'Lào Cai'),
('SV054', N'Phạm Thị Yến Nhi', N'Du lịch', '0912345040', 'D102', N'Nữ', '2003-08-09', '2023-10-15', N'Hòa Bình'),
('SV056', N'Trần Thị Hồng Nhung', N'Tài chính - Ngân hàng', '0912345042', 'D102', N'Nữ', '2004-08-22', '2024-12-05', N'Quảng Ngãi'),
('SV058', N'Phạm Thị Thu Trang', N'Kinh tế', '0912345044', 'D102', N'Nữ', '2003-11-09', '2023-10-15', N'Gia Lai'),
-- D103 (4 SV)
('SV060', N'Vũ Thị Hồng Hạnh', N'Công nghệ sinh học', '0912345046', 'D103', N'Nữ', '2004-09-14', '2024-09-28', N'Thái Nguyên'),
('SV062', N'Nguyễn Thị Hồng', N'Ngôn ngữ Anh', '0912345048', 'D103', N'Nữ', '2003-03-22', '2023-11-05', N'Quảng Ngãi'),
('SV064', N'Phạm Thị Mai', N'Marketing', '0912345050', 'D103', N'Nữ', '2004-11-09', '2024-12-15', N'Phú Thọ'),
('SV066', N'Vũ Thị Hạnh', N'Du lịch', '0912345052', 'D103', N'Nữ', '2003-09-14', '2023-10-28', N'Lai Châu'),
-- D104 (4 SV)
('SV068', N'Nguyễn Thị Hương', N'Luật', '0912345054', 'D104', N'Nữ', '2004-06-19', '2024-09-20', N'Bình Định'),
('SV070', N'Lê Thị Ngọc', N'Kinh tế', '0912345056', 'D104', N'Nữ', '2003-12-12', '2023-12-10', N'Khánh Hòa'),
('SV072', N'Phạm Thị Thảo', N'Công nghệ sinh học', '0912345058', 'D104', N'Nữ', '2004-10-21', '2024-10-25', N'Bến Tre'),
('SV074', N'Trần Thị Thanh', N'Ngôn ngữ Anh', '0912345060', 'D104', N'Nữ', '2003-07-07', '2023-09-28', N'Hà Nam');
GO




----------------------------------------------------
-- 5. BẢNG TÀI KHOẢN (Độc lập - Dùng cho đăng nhập)
----------------------------------------------------
IF OBJECT_ID('TaiKhoan', 'U') IS NOT NULL DROP TABLE TaiKhoan;
GO

CREATE TABLE TaiKhoan (
    UserID INT PRIMARY KEY IDENTITY(1,1), -- PK
    TenDangNhap VARCHAR(50) NOT NULL UNIQUE,
    MatKhau VARCHAR(255) NOT NULL,
    ChucVu NVARCHAR(20) NOT NULL 
        CHECK (ChucVu IN (N'Quản lý', N'Sinh viên'))
);
GO

-- Dữ liệu mẫu (Tên đăng nhập trùng với mã quản lý/mssv để tiện quản lý)
INSERT INTO TaiKhoan (TenDangNhap, MatKhau, ChucVu)
SELECT 
    MSSV AS TenDangNhap,
    -- Lấy 3 ký tự cuối của MSSV (ví dụ: 'SV001' -> '001')
    SUBSTRING(MSSV, 3, 3) AS MatKhau, 
    N'Sinh viên' AS ChucVu
FROM 
    SinhVien;
GO

INSERT INTO TaiKhoan (TenDangNhap, MatKhau, ChucVu)
SELECT 
    MaQuanLy AS TenDangNhap,
    -- Lấy 3 ký tự cuối của MaQuanLy (ví dụ: 'QL001' -> '001')
    SUBSTRING(MaQuanLy, 3, 3) AS MatKhau, 
    N'Quản lý' AS ChucVu
FROM 
    QuanLy;
GO

ALTER TABLE SinhVien
ADD TrangThaiTienPhong NVARCHAR(20) DEFAULT N'Chưa đóng'; -- Mặc định là 'Chưa đóng'
GO

CREATE TABLE LichSuDongTien (
    MaThanhToan INT PRIMARY KEY IDENTITY(1,1), -- Mã giao dịch tự tăng
    MSSV VARCHAR(20) NOT NULL,                 -- Mã SV đã đóng
    ThangDongTien INT NOT NULL,                -- Đóng cho tháng nào (VD: 10)
    NamDongTien INT NOT NULL,                  -- Đóng cho năm nào (VD: 2025)
    SoTien DECIMAL(10, 2) NOT NULL,            -- Số tiền đã đóng
    NgayDong DATE NOT NULL,                    -- Ngày thực tế đóng tiền
    
    -- Tạo khóa ngoại liên kết với bảng SinhVien
    FOREIGN KEY (MSSV) REFERENCES SinhVien(MSSV)
        ON DELETE CASCADE -- Nếu xóa SV thì xóa luôn lịch sử đóng tiền
);
GO




