from . import dao
from app.modules.fields import dao as field_dao
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def caculator_total_price(booking_date, start_time, end_time, field):
    total_price = 0.0
    field_prices = dao.get_field_prices(field=field, date_selected=booking_date)
    
    start = datetime.combine(booking_date, start_time)
    end = datetime.combine(booking_date, end_time)

    for fp in field_prices:
        start_fp = datetime.combine(booking_date, fp.start_time)
        end_fp = datetime.combine(booking_date, fp.end_time)

        overlap_start = max(start, start_fp)
        overlap_end = min(end, end_fp)

        seconds = (overlap_end - overlap_start).total_seconds()
        if seconds > 0:
            hours = seconds/3600
            total_price += (hours * fp.price)

    return total_price


def create_booking_service(field_id, user_id, data):
    try:
        booking_date = data.get("booking_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        is_overlap = dao.check_booking_overlap(field_id, booking_date, start_time, end_time)
        if is_overlap:
            raise ValidationError("Khung giờ này đã có người đặt")

        field = field_dao.get_field_by_id(field_id= field_id)
        total_price = caculator_total_price(booking_date= booking_date, start_time=start_time, end_time=end_time, field=field)

        booking = dao.create_booking(field_id= field_id, user_id=user_id, total_price=total_price, data=data)

        return booking
    
    except IntegrityError:
        raise ValidationError("Dữ liệu vi phạm ràng buộc database")