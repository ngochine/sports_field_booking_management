from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_fields, sample_field_price, sample_booking
from app.modules.bookings.dao import (get_field_prices, check_booking_overlap, check_booking_limit, check_future_booking,
                                      get_booking_by_id, create_booking, update_booking_status)
from app.modules.bookings.models import FieldPrice, Booking, BookingStatusEnum
from datetime import date, time, datetime
from sqlalchemy import and_
import pytest
from sqlalchemy.exc import IntegrityError


def test_get_field_prices(test_session, sample_field_price, sample_fields):
    field_prices = get_field_prices(field= sample_fields[1])
    assert field_prices.count() == 2
    assert (field_prices.count() == FieldPrice.query.filter(FieldPrice.field == sample_fields[1])
            .filter(and_(FieldPrice.day_of_week == None, FieldPrice.special_date == None)).count())

    field_prices = get_field_prices(field=sample_fields[0], date_selected=date(2026, 4, 30))
    assert field_prices.count() == 1
    assert (field_prices.count() == FieldPrice.query.filter(FieldPrice.field == sample_fields[0])
            .filter(FieldPrice.special_date == date(2026, 4, 30)).count())

    field_prices = get_field_prices(field=sample_fields[0], date_selected=date(2026, 5, 17))
    assert field_prices.count() == 1
    assert (field_prices.count() == FieldPrice.query.filter(FieldPrice.field == sample_fields[0])
            .filter(FieldPrice.day_of_week == 6).count())


def test_check_booking_overlap(test_session, sample_booking, sample_fields):
    is_overlap = check_booking_overlap(field_id=sample_booking[0].field_id,
                                       date_selected=sample_booking[0].booking_date,
                                       start_time=sample_booking[0].start_time,
                                       end_time=sample_booking[0].end_time)
    assert is_overlap

    is_overlap = check_booking_overlap(field_id=sample_booking[0].field_id,
                                       date_selected=sample_booking[0].booking_date,
                                       start_time=time(18, 00),
                                       end_time=time(19, 00))
    assert is_overlap

    is_overlap = check_booking_overlap(field_id=sample_booking[0].field_id,
                                       date_selected=sample_booking[0].booking_date,
                                       start_time=time(7, 00),
                                       end_time=time(18, 30))
    assert not is_overlap


def test_check_booking_limit(test_session, sample_booking):
    is_limit = check_booking_limit(user_id=1, booking_date=sample_booking[0].booking_date)
    assert is_limit

    is_limit = check_booking_limit(user_id=1000, booking_date=sample_booking[0].booking_date)
    assert not is_limit

    is_limit = check_booking_limit(user_id=2, booking_date=datetime.today().date())
    assert not is_limit


def test_check_future_booking(test_session, sample_fields, sample_booking):
    field = sample_fields[0]
    result = check_future_booking(field)
    assert result

    field = sample_fields[3]
    result = check_future_booking(field)
    assert not result


def test_get_booking_by_id(test_session, sample_booking):
    booking = get_booking_by_id(booking_id=1)
    assert booking.id == 1

    booking = get_booking_by_id(booking_id=2)
    assert booking.id == Booking.query.get(2).id

    booking = get_booking_by_id(booking_id=1000)
    assert not booking


def test_update_booking_status(test_session, sample_booking):
    booking = sample_booking[2]
    assert booking.status == BookingStatusEnum.PENDING

    booking = update_booking_status(booking=booking, status=BookingStatusEnum.PAID)
    assert booking.status == BookingStatusEnum.PAID

    booking = update_booking_status(booking=booking,status=BookingStatusEnum.CANCELLED)
    assert booking.status == BookingStatusEnum.CANCELLED


def test_create_booking(test_session, sample_fields):
    field = sample_fields[0]
    data = {
        "booking_date": date(2026, 5, 18),
        "start_time": time(18, 0),
        "end_time": time(20, 0),
        "status": BookingStatusEnum.PENDING
    }

    booking = create_booking(field_id=field.id, user_id=1, total_price=250000, data=data)

    assert booking is not None
    assert booking.field_id == field.id
    assert booking.user_id == "1"
    assert booking.total_price == 250000
    assert booking.status == BookingStatusEnum.PENDING
    assert booking.booking_date == date(2026, 5, 18)
    assert booking.start_time == time(18, 0)
    assert booking.end_time == time(20, 0)

    with pytest.raises(IntegrityError):
        create_booking(field_id=None, user_id=1, total_price=250000, data=data)

    assert Booking.query.count() == 1