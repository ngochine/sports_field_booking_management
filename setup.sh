if [ -f "venv/Scripts/activate" ]; then
    echo "Đã tồn tại môi trường ảo"
else
    echo "Tạo môi trường ảo"
    python -m venv venv
fi

source venv/Scripts/activate

echo "Cài đặt các thư viện từ requirements.txt"
pip install -r requirements.txt

if [ -f ".env" ]; then
    if grep -q "^SECRET_KEY=" .env; then
        echo "SECRET_KEY đã tồn tại trong .env"
    else
        echo "Tạo SECRET_KEY và thêm vào .env"
        SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
        echo "SECRET_KEY=$SECRET_KEY" >> .env
    fi
fi

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