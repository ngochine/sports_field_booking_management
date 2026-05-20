from . import dao
from app.common.tasks import trigger_task, task_auto_cancelled_booking
from app.modules.fields import dao as field_dao
from app.modules.transactions import dao as transaction_dao
from app.modules.bookings.models import BookingStatusEnum
from app.modules.fields.models import FieldStatusEnum, Field
from app.modules.auth.models import User

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.exceptions import Forbidden, NotFound

from datetime import datetime, timedelta
import math
from flask import current_app
from app.extension import db


def caculator_total_time(booking_date, start_time, end_time):
    start = datetime.combine(booking_date, start_time)
    end = datetime.combine(booking_date, end_time)

    return (end - start).total_seconds() / 3600


def caculator_total_price(booking_date, start_time, end_time, field):
    total_price = 0.0
    field_prices = dao.get_field_prices(field=field, date_selected=booking_date)
    
    start = datetime.combine(booking_date, start_time)
    end = datetime.combine(booking_date, end_time)

    cover_seconds = 0.0
    for fp in field_prices:
        start_fp = datetime.combine(booking_date, fp.start_time)
        end_fp = datetime.combine(booking_date, fp.end_time)

        overlap_start = max(start, start_fp)
        overlap_end = min(end, end_fp)

        seconds = (overlap_end - overlap_start).total_seconds()
        if seconds > 0:
            cover_seconds += seconds
            hours = seconds/3600
            total_price += (float(hours) * float(fp.price))

    if cover_seconds < (end-start).total_seconds():
        raise ValidationError("Khung giờ này chưa được cấu hình giá")
    return total_price


def create_booking_service(field_id, user_id, data):
    try:
        booking_date = data.get("booking_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        field = field_dao.get_field_by_id(field_id=field_id)
        if field is None:
            raise NotFound("Sân không tồn tại")

        if field.status == FieldStatusEnum.DELETED:
            raise NotFound("Sân không tồn tại")

        user = User.query.filter_by(id=user_id).with_for_update().first()
        field = Field.query.filter_by(id=field_id).with_for_update().first()

        is_overlap = dao.check_booking_overlap(field.id, booking_date, start_time, end_time)
        if is_overlap:
            db.session.rollback()
            raise ValidationError("Khung giờ đặt bị trùng")

        is_limit = dao.check_booking_limit(user_id, created_date= datetime.now().date())
        if is_limit:
            db.session.rollback()
            raise ValidationError("Tài khoản đã đạt giới hạn đặt trong ngày (3 lần/ngày)")

        total_price = caculator_total_price(booking_date= booking_date, start_time=start_time, end_time=end_time, field=field)

        booking = dao.create_booking(field_id= field.id, user_id=user_id, total_price=total_price, data=data)
        db.session.add(booking)
        db.session.commit()

        trigger_task(func=task_auto_cancelled_booking, run_date=datetime.now() + timedelta(minutes=15), args=[booking.id])

        return booking

    except IntegrityError:
        db.session.rollback()
        raise ValidationError("Dữ liệu vi phạm ràng buộc database")

    except OperationalError:
        db.session.rollback()
        raise ValidationError("Hệ thống đang xử lý nhiều yêu cầu, vui lòng thử lại")


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
    if booking.user_id != user_id:
        raise Forbidden("Booking này không phải của bạn, bạn không có quyền huỷ")

    if booking.status not in [BookingStatusEnum.PENDING, BookingStatusEnum.PAID]:
        raise ValidationError("Chỉ được huỷ khi booking có trạng thái PENDING hoặc PAID")

    start_datetime = datetime.combine(booking.booking_date, booking.start_time)
    end_datetime = datetime.combine(booking.booking_date, booking.end_time)

    if start_datetime <= datetime.now() <= end_datetime:
        raise ValidationError("Không được huỷ nếu sân đang trong thời gian sử dụng")

    if end_datetime <= datetime.now():
        raise ValidationError("Không được huỷ booking đã kết thúc")

    diff = (start_datetime - datetime.now()).total_seconds() / 3600
    if diff < 2:
        raise ValidationError("Không được huỷ khi còn dưới 2 giờ trước giờ chơi")


def cancelled_booking_service(booking_id, user_id, data: dict):
    status = data.get("status")
    if status != BookingStatusEnum.CANCELLED.name:
        raise ValidationError({"status": ["Chỉ được phép huỷ booking"]})

    booking = dao.get_booking_by_id(booking_id=booking_id)
    if booking is None:
        raise NotFound("Không tồn tại booking")

    validate_cancelled_booking(booking, user_id)
    booking = dao.update_booking_status(booking = booking, status= BookingStatusEnum.CANCELLED)

    return booking


def get_booking_detail_service(booking_id, user_id):
    booking = dao.get_booking_by_id(booking_id=booking_id)

    if booking is None:
        raise NotFound("Không tồn tại booking")

    if booking.user_id != user_id:
        raise Forbidden("Booking này không phải của bạn, bạn không có quyền xem")

    latest_transaction = transaction_dao.get_latest_transaction_by_booking(booking=booking)

    return {
        'booking': booking,
        'latest_transaction': latest_transaction,
    }