from app.modules.fields.models import FieldStatusEnum
from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_fields, sample_field_price, sample_booking
import pytest
from datetime import date, time, timedelta, datetime
import re
from werkzeug.exceptions import NotFound, Forbidden
from marshmallow import ValidationError
from app.modules.bookings.models import BookingStatusEnum, Booking
from app.modules.bookings.services import (caculator_total_time, caculator_total_price, create_booking_service,
                                           get_list_booking_service, cancelled_booking_service, get_booking_detail_service)


def test_caculator_total_time_service():
    total_time = caculator_total_time(booking_date=date.today(),
                                      start_time=time(7, 30), end_time=time(7, 30))
    assert total_time == 0

    total_time = caculator_total_time(booking_date=date.today(),
                                      start_time=time(7, 30), end_time=time(9, 00))
    assert total_time == 1.5


def test_caculator_total_price_service(sample_field_price, sample_fields):
    total_price = caculator_total_price(booking_date=date(2026, 4, 30),
                                        start_time=time(7, 00), end_time=time(9, 00), field=sample_fields[0])

    assert total_price == 1000000

    with pytest.raises(ValidationError, match="Khung giờ này chưa được cấu hình giá"):
        caculator_total_price(booking_date=date.today(),
                              start_time=time(9, 00), end_time=time(10, 00), field=sample_fields[1])


def test_get_list_booking_service(test_session, sample_booking):
    result = get_list_booking_service(user_id="1", filters={})
    assert result["bookings"] is not None
    assert len(result["bookings"]) == 2
    assert result["page"] == 1
    assert result["pages"] == 2
    assert all(booking.user_id == "1" for booking in result["bookings"])

    result = get_list_booking_service(user_id="1",
        filters={
            "status": BookingStatusEnum.PAID
        }
    )
    assert len(result["bookings"]) == 2
    assert all(booking.status == BookingStatusEnum.PAID for booking in result["bookings"])

    result = get_list_booking_service(user_id="3",
        filters={
            "status": BookingStatusEnum.CANCELLED
        }
    )
    assert len(result["bookings"]) == 2
    assert all(booking.status == BookingStatusEnum.CANCELLED for booking in result["bookings"])

    result = get_list_booking_service(user_id="99999", filters={})
    assert len(result["bookings"]) == 0
    assert result["page"] == 1
    assert result["pages"] == 0


def test_create_booking_service_success(sample_fields, sample_field_price):
    data = {
        "booking_date": date.today(),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
    }
    booking = create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)
    assert booking.user_id == "1"
    assert booking.booking_date == data["booking_date"]
    assert booking.start_time == data["start_time"]
    assert booking.end_time == data["end_time"]
    assert booking.status == BookingStatusEnum.PENDING
    assert Booking.query.count() == 1


def test_create_booking_service_fail(test_session, sample_fields, sample_field_price):
    data = {
        "booking_date": date.today(),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
    }
    booking = create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)
    assert booking is not None

    with pytest.raises(ValidationError, match="Khung giờ đặt bị trùng"):
        create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)

    with pytest.raises(NotFound, match="Sân không tồn tại"):
        create_booking_service(field_id=99999, user_id="1", data=data)

    with pytest.raises(NotFound, match="Sân không tồn tại"):
        field = sample_fields[2]
        field.status = FieldStatusEnum.DELETED
        test_session.commit()

        create_booking_service(field_id=sample_fields[2].id, user_id="1", data=data)

    data = {
        "booking_date": date.today(),
        "start_time": time(12, 0),
        "end_time": time(13, 0),
    }
    create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)

    data = {
        "booking_date": date.today(),
        "start_time": time(13, 30),
        "end_time": time(15, 0),
    }
    create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)
    assert Booking.query.count() == 3

    data = {
        "booking_date": date.today(),
        "start_time": time(16, 00),
        "end_time": time(17, 0),
    }
    with pytest.raises(ValidationError, match=re.escape("Tài khoản đã đạt giới hạn đặt trong ngày (3 lần/ngày)")):
        create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)

    data = {
        "booking_date": date.today(),
        "start_time": time(17, 00),
        "end_time": time(18, 0),
    }
    with pytest.raises(ValidationError, match=re.escape("Dữ liệu vi phạm ràng buộc database")):
        create_booking_service(field_id=sample_fields[0].id, user_id=None, data=data)


def test_cancelled_booking_service_success(test_session, sample_fields, sample_field_price):
    data = {
        "booking_date": (datetime.now() + timedelta(days=1)),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
    }
    booking = create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)
    assert booking.status == BookingStatusEnum.PENDING
    assert booking.user_id == "1"
    assert booking.id == 1

    cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.CANCELLED.name})
    assert booking.status == BookingStatusEnum.CANCELLED


def test_cancelled_booking_service_fail(test_session, sample_fields, sample_field_price):
    with pytest.raises(NotFound, match="Không tồn tại booking"):
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.CANCELLED.name})

    with pytest.raises(ValidationError) as e:
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.PAID.name})
    assert e.value.messages == {
        "status": ["Chỉ được phép huỷ booking"]
    }

    with pytest.raises(ValidationError) as e:
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.PENDING.name})
    assert e.value.messages == {
        "status": ["Chỉ được phép huỷ booking"]
    }

    data = {
        "booking_date": (datetime.now() + timedelta(days=1)),
        "start_time": time(18, 30),
        "end_time": time(20, 0),
    }
    booking = create_booking_service(field_id=sample_fields[0].id, user_id="1", data=data)
    assert booking.status == BookingStatusEnum.PENDING
    assert booking.user_id == "1"
    assert booking.id == 1

    with pytest.raises(Forbidden, match="Booking này không phải của bạn, bạn không có quyền huỷ"):
        cancelled_booking_service(booking_id=1, user_id="2", data={"status": BookingStatusEnum.CANCELLED.name})

    with pytest.raises(ValidationError, match="Chỉ được huỷ khi booking có trạng thái PENDING hoặc PAID"):
        booking.status = BookingStatusEnum.CANCELLED
        test_session.commit()
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.CANCELLED.name})

    with pytest.raises(ValidationError, match="Không được huỷ nếu sân đang trong thời gian sử dụng"):
        booking.status = BookingStatusEnum.PENDING
        booking.booking_date = date.today()
        booking.start_time = datetime.now().time()
        booking.end_time = (datetime.now() + timedelta(minutes=60)).time()
        test_session.commit()
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.CANCELLED.name})

    with pytest.raises(ValidationError, match="Không được huỷ booking đã kết thúc"):
        booking.booking_date = date.today() - timedelta(days=1)
        test_session.commit()
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.CANCELLED.name})

    with pytest.raises(ValidationError, match="Không được huỷ khi còn dưới 2 giờ trước giờ chơi"):
        booking.booking_date = date.today()
        booking.start_time = (datetime.now() + timedelta(hours=0.5)).time()
        booking.end_time = (datetime.now() + timedelta(hours=1.5)).time()
        test_session.commit()
        cancelled_booking_service(booking_id=1, user_id="1", data={"status": BookingStatusEnum.CANCELLED.name})


    assert booking.status == BookingStatusEnum.PENDING


def test_get_booking_detail_service_fail(test_session, sample_booking):
    with pytest.raises(NotFound, match="Không tồn tại booking"):
        get_booking_detail_service(booking_id=1000, user_id="1")

    with pytest.raises(Forbidden, match="Booking này không phải của bạn, bạn không có quyền xem"):
        get_booking_detail_service(booking_id=sample_booking[0].id, user_id="999")
        result = get_booking_detail_service(booking_id=sample_booking[0].id, user_id="1")

        assert result is not None
        assert result["booking"] is not None
        assert result["booking"].id == sample_booking[0].id
        assert result["booking"].user_id == "1"
        assert "latest_transaction" in result


def test_get_booking_detail_service_success(test_session, sample_booking):
    result = get_booking_detail_service(booking_id=sample_booking[0].id,user_id="1")

    booking = result["booking"]
    latest_transaction = result["latest_transaction"]

    assert result is not None
    assert booking.id == sample_booking[0].id
    assert booking.user_id == "1"
    assert booking.status == sample_booking[0].status
    assert booking.total_price == sample_booking[0].total_price
    assert latest_transaction is None