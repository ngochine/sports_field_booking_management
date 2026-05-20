from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_booking
from datetime import datetime, timedelta
import time
from app.common.tasks import scheduler, trigger_task, task_auto_update_transaction_status
from app.modules.transactions.models import TransactionStatusEnum, Transaction, TransactionMethodEnum
from app.modules.transactions import dao as transaction_dao


def test_auto_cancelled_booking_task(test_session, sample_booking, test_app):
    transaction = Transaction(
        booking=sample_booking[0],
        amount=sample_booking[0].total_price,
        method=TransactionMethodEnum.VNPAY,
        payment_url='https://example.com',
        app_trans_id = "hwgkjqmeb"
    )
    test_session.add(transaction)
    test_session.commit()

    scheduler.app = test_app

    if not scheduler.running:
        scheduler.start()

    run_date = datetime.now() + timedelta(seconds=1)

    trigger_task(func=task_auto_update_transaction_status, run_date=run_date, args=[transaction.id])

    time.sleep(2)
    test_session.refresh(transaction)

    updated_transaction = transaction_dao.get_transaction_by_id(transaction_id=transaction.id)
    assert updated_transaction.status == TransactionStatusEnum.FAILED

    scheduler.remove_all_jobs()