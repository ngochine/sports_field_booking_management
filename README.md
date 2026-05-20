# Hệ thống QUẢN LÝ ĐẶT SÂN THỂ THAO (Sport Field Booking Management)
## Mô tả 
Dự án phục vụ cho bài tập lớn môn Kiểm thử phần mềm, cho phép người dùng xem, đặt/huỷ/thanh toán sân thể thao theo khung giờ. Quá trình kiểm thử sẽ theo quy trình từ kiểm thử unit test, integration test, system test đến acceptance test để đảm bảo chất lượng.

## Thành viên nhóm
| MSSV | Họ tên | Vai trò                 |
|------|--------|-------------------------|
| 2351050189 | Hồ Thị Ngọc Trinh | Nhóm trưởng + Developer |
| 2351050165 | Bùi Thiên Hương Thảo | Thành viên + Tester     |

## Công nghệ sử dụng
- **Backend**: Python Flask Framework  
- **Authentication**: JWT Authentication
- **Frontend**: HTML + CSS + JavaScript + Bootstrap Framework
- **Database**: MySQL  
- **Version control**: Git + GitHub
- **Deployment**: PythonAnyWhere (Dự tính)

## Cấu trúc thư mục
```bash
sports_field_booking_management_team8
├── .github/
│   └── workflows/ 
├── app/
│   ├── admin/
│   ├── common/
│   ├── fixtures/
│   ├── modules/
│   │   ├── auth/
│   │   ├── bookings/
│   │   ├── fields/
│   │   ├── transactions/
│   │   └── __init__.py
│   ├── static/
│   ├── templates/
│   ├── extension.py
│   ├── insertdb.py
│   └── __init__.py
├── docs/
├── instances/
├── migrations/
├── tests/
│   ├── integration/
│   ├── selenium/
│   ├── unit/
│   ├── sample_fixtures.py
│   ├── test_base.py
│   ├── test_performance.py
│   └── __init__.py
├── LICENSE
├── README.md
├── requirements.txt
├── run.py
└── setup.sh
```

## Chạy và cài đặt
1. Tải dự án về máy
```
git clone "https://github.com/ngochine/sports_field_booking_management_team8.git"
```
2. Chạy ứng dụng 
```
chmod +x setup.sh
```

## Truy cập
- Local: http://localhost:5000
- Production: [Chưa cập nhật]

## Tài liệu
- [Diagram](docs/diagram)
- [Api test](docs/postman)
- [Selenium test](docs/screenshots/selenium)
- [Coverage test](docs/coverage)
- [Performance test](docs/performance)