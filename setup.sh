if [ -f "venv/Scripts/activate" ]; then
    echo "Đã tồn tại môi trường ảo"
else
    echo "Tạo môi trường ảo"
    python -m venv venv
fi

source venv/Scripts/activate

echo "Cài đặt các thư viện từ requirements.txt"
pip install -r requirements.txt

if [ -d "migrations" ]; then
    echo "Đã tồn tại migrations"
    echo "Thực thi migrate cơ sở dữ liệu"
    flask db upgrade
else
    echo "Tạo migrations cơ sở dữ liệu"
    flask db init
    flask db migrate -m "init"
    flask db upgrade
fi

echo "Chèn dữ liệu mẫu"
python -m app.insertdb

echo "Khởi chạy server"
python ./run.py