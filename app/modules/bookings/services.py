from . import dao
from app.modules.fields import dao as field_dao
from app.modules.bookings.models import BookingStatusEnum
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import math
from flask import current_app


def caculator_total_time(booking_date, start_time, end_time):
    start = datetime.combine(booking_date, start_time)
    end = datetime.combine(booking_date, end_time)

    return (end - start).total_seconds() / 3600


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
            total_price += (float(hours) * float(fp.price))

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
        if field is None:
            raise ValidationError("Sân không tồn tại")

        is_limit = dao.check_booking_limit(user_id, booking_date)
        if is_limit:
            raise ValidationError("Tài khoản đã đạt giới hạn đặt trong ngày (3 lần/ngày)")

        total_price = caculator_total_price(booking_date= booking_date, start_time=start_time, end_time=end_time, field=field)

        booking = dao.create_booking(field_id= field_id, user_id=user_id, total_price=total_price, data=data)

        return booking
    
    except IntegrityError:
        raise ValidationError("Dữ liệu vi phạm ràng buộc database")
    

def get_list_booking_service(user_id: str, filters: dict):
    page = filters.get('page', 1)
    status = filters.get('status', "all")

    bookings = dao.get_bookings_by_user(user_id=user_id, page=page, status=status)
    pages = math.ceil(len(dao.get_bookings_by_user(user_id=user_id, status=status))/current_app.config["PAGE_SIZE"])

    return {
        'bookings': bookings,
        'pages': pages,
        'page': int(page) if page else 1
    }


def validate_cancelled_booking(booking, user_id):
    try: 
        if booking is None:
            raise ValueError
        
        if booking.user_id != user_id:
            raise PermissionError("Booking này không phải của bạn, bạn không có quyền huỷ")
        
        if booking.status not in [BookingStatusEnum.PENDING, BookingStatusEnum.PAID]:
            raise ValidationError("Chỉ được huỷ khi booking có trạng thái PENDING hoặc PAID")
        
        start_datetime = datetime.combine(booking.booking_date, booking.start_time)
        end_datetime = datetime.combine(booking.booking_date, booking.end_time)

        if start_datetime <= datetime.now() <= end_datetime:
            raise ValidationError("Không được huỷ nếu sân đang được sử dụng")
        
        diff = (start_datetime - datetime.today()).total_seconds()/3600
        if diff < 2:
            raise ValidationError("Không được huỷ khi còn dưới 2 giờ trước giờ chơi")

    except ValueError:
        raise ValidationError("Không tồn tại booking")


def cancelled_booking_service(booking_id, user_id, data: dict):
    booking = dao.get_booking_by_id(booking_id=booking_id)
    validate_cancelled_booking(booking, user_id)

    status = data.get("status")

    booking = dao.update_booking_status(booking, status)
    return booking