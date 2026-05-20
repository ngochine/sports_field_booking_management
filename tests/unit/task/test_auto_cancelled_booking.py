from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_booking
from datetime import datetime, timedelta
import time
from app.common.tasks import scheduler, trigger_task, task_auto_cancelled_booking
from app.modules.bookings.models import BookingStatusEnum
from app.modules.bookings import dao as booking_dao


def test_auto_cancelled_booking_task(test_session, sample_booking, test_app):
    booking = sample_booking[0]
    booking.status = BookingStatusEnum.PENDING
    test_session.commit()

    scheduler.app = test_app

    if not scheduler.running:
        scheduler.start()

    run_date = datetime.now() + timedelta(seconds=1)

    trigger_task(func=task_auto_cancelled_booking, run_date=run_date, args=[booking.id])

    time.sleep(2)
    test_session.refresh(booking)

    updated_booking = booking_dao.get_booking_by_id(booking_id=booking.id)
    assert updated_booking.status == BookingStatusEnum.CANCELLED

    scheduler.remove_all_jobs()