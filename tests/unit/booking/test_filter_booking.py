from tests.test_base import test_app, test_session
from tests.unit.sample_fixtures import sample_booking
from app.modules.bookings.dao import get_bookings_by_user


def test_load_all_booking(sample_booking):
    actual_booking = get_bookings_by_user(user_id=1)

    assert len(actual_booking) == len([b for b in sample_booking if b.user_id == str(1)])


def test_paging(sample_booking):
    actual_booking = get_bookings_by_user(user_id=1, page=2)
    assert len(actual_booking) == 1

    actual_booking = get_bookings_by_user(user_id=1, page=3)
    assert len(actual_booking) == 0


def test_status(sample_booking):
    actual_booking_pending = get_bookings_by_user(user_id=1, status="PENDING")
    assert len(actual_booking_pending) == 0

    actual_booking_paid = get_bookings_by_user(user_id=1, status="PAID")
    assert len(actual_booking_paid) == 3

    actual_booking_cancel = get_bookings_by_user(user_id=1, status="CANCELLED")
    assert len(actual_booking_cancel) == 0

    assert len(get_bookings_by_user(user_id=1)) == len(actual_booking_pending) + len(actual_booking_paid) + len(actual_booking_cancel)


def test_page_status(sample_booking):
    actual_booking = get_bookings_by_user(user_id=1, page=2, status="PENDING")
    assert len(actual_booking) == 0

    actual_booking = get_bookings_by_user(user_id=1, page=2, status="PAID")
    assert len(actual_booking) == 1


def test_booking_order_desc(sample_booking):
    actual_booking = get_bookings_by_user(user_id=1)

    for i in range(len(actual_booking) - 1):
        assert actual_booking[i].created_at >= actual_booking[i + 1].created_at