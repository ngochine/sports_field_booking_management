from app import create_app
from app.extension import db
from flask import json

from app.modules.auth.models import *
from app.modules.fields.models import *
from app.modules.bookings.models import *
from app.modules.transactions.models import *

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        def load_data(file, model):
            with open(file, encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for item in data:
                        db.session.add(model(**item))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print("Lỗi:", e)

        load_data("app/fixtures/user.json", User)
        load_data("app/fixtures/field_type.json", FieldType)
        load_data("app/fixtures/address.json", Address)
        load_data("app/fixtures/location.json", Location)
        load_data("app/fixtures/field.json", Field)
        load_data("app/fixtures/field_price.json", FieldPrice)
        load_data("app/fixtures/booking.json", Booking)
        load_data("app/fixtures/review.json", Review)
        load_data("app/fixtures/report.json", Report)
        load_data("app/fixtures/transaction.json", Transaction)

        print("Đã load xong tất cả dữ liệu")