from app.modules.transactions.models import Transaction, TransactionStatusEnum, TransactionMethodEnum
from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_booking
from app.modules.transactions.dao import create_transaction, update_transaction_status, update_transaction, get_transaction_by_id


def test_create_transaction(test_session, sample_booking):
    transaction = create_transaction(booking=sample_booking[0])

    assert transaction.booking_id == sample_booking[0].id
    assert transaction.app_trans_id == f"BOOKING_{sample_booking[0].id}"
    assert transaction.status == TransactionStatusEnum.PENDING
    assert transaction.method == TransactionMethodEnum.VNPAY
    assert transaction.amount == sample_booking[0].total_price
    assert Transaction.query.count() == 1


def test_get_transaction_by_id(test_session, sample_booking):
    transaction= create_transaction(booking=sample_booking[0])

    assert get_transaction_by_id(transaction_id=1) == transaction
    assert get_transaction_by_id(transaction_id=1000) is None


def test_update_transaction_status(test_session, sample_booking):
    transaction = create_transaction(booking=sample_booking[0])
    assert Transaction.query.count() == 1
    assert transaction.status == TransactionStatusEnum.PENDING
    assert transaction.paid_at is None

    transaction = update_transaction_status(transaction=transaction, status=TransactionStatusEnum.FAILED)
    assert transaction.status == TransactionStatusEnum.FAILED
    assert transaction.paid_at is None

    transaction = update_transaction_status(transaction=transaction, status=TransactionStatusEnum.SUCCESS)
    assert transaction.status == TransactionStatusEnum.SUCCESS
    assert transaction.paid_at is not None


def test_update_transaction(test_session, sample_booking):
    transaction = create_transaction(booking=sample_booking[0])
    assert transaction.payment_url is None

    transaction = update_transaction(transaction=transaction, payment_url="https://example.com")
    assert transaction.payment_url == "https://example.com"