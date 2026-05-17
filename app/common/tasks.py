from apscheduler.schedulers.background import BackgroundScheduler
from app.extension import db
from app.modules.bookings.models import BookingStatusEnum
from app.modules.bookings import dao as booking_dao
from app.modules.transactions import dao as transaction_dao
from app.modules.transactions.models import TransactionStatusEnum


scheduler = BackgroundScheduler()

def init_scheduler(app):
    if app.config.get("TESTING"):
        scheduler.app = app
        return

    if not scheduler.running:
        scheduler.app = app
        scheduler.start()


def task_auto_cancelled_booking(booking_id, app):
    with app.app_context():
        booking = booking_dao.get_booking_by_id(booking_id=booking_id)
        if booking and booking.status == BookingStatusEnum.PENDING:
            booking_dao.update_booking_status(booking=booking, status=BookingStatusEnum.CANCELLED)


def task_auto_update_transaction_status(transaction_id, app):
    with app.app_context():
        transaction = transaction_dao.get_transaction_by_id(transaction_id= transaction_id)
        if transaction and transaction.status == TransactionStatusEnum.PENDING:
            transaction_dao.update_transaction_status(transaction=transaction, status=TransactionStatusEnum.FAILED)


def trigger_task(func, run_date, args=None):
    if args is None:
        args = []

    scheduler.add_job(
        func=func,
        trigger="date",
        run_date=run_date,
        args=args + [scheduler.app]
    )