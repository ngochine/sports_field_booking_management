from app.modules.transactions.models import Transaction, TransactionStatusEnum, TransactionMethodEnum
from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_booking
from app.modules.transactions.dao import (create_transaction, update_transaction_status, get_transaction_by_id,
                                          get_transaction_by_app_trans_id, get_latest_transaction_by_booking)


def test_create_transaction(test_session, sample_booking):
    transaction = create_transaction(booking=sample_booking[0], app_trans_id=f"BOOKING_{sample_booking[0].id}",
                                     payment_url="http://example.com")

    assert transaction.booking_id == sample_booking[0].id
    assert transaction.app_trans_id == f"BOOKING_{sample_booking[0].id}"
    assert transaction.status == TransactionStatusEnum.PENDING
    assert transaction.method == TransactionMethodEnum.VNPAY
    assert transaction.amount == sample_booking[0].total_price
    assert transaction.app_trans_id == f"BOOKING_{sample_booking[0].id}"
    assert transaction.payment_url == "http://example.com"
    assert Transaction.query.count() == 1


def test_get_transaction_by_id(test_session, sample_booking):
    transaction= create_transaction(booking=sample_booking[0], app_trans_id=f"BOOKING_{sample_booking[0].id}",
                                    payment_url="http://example.com")

    assert get_transaction_by_id(transaction_id=1) == transaction
    assert get_transaction_by_id(transaction_id=1000) is None


def test_update_transaction_status(test_session, sample_booking):
    transaction = create_transaction(booking=sample_booking[0], app_trans_id=f"BOOKING_{sample_booking[0].id}",
                                     payment_url="http://example.com")
    assert Transaction.query.count() == 1
    assert transaction.status == TransactionStatusEnum.PENDING
    assert transaction.paid_at is None

    transaction = update_transaction_status(transaction=transaction, status=TransactionStatusEnum.FAILED)
    assert transaction.status == TransactionStatusEnum.FAILED
    assert transaction.paid_at is None

    transaction = update_transaction_status(transaction=transaction, status=TransactionStatusEnum.SUCCESS)
    assert transaction.status == TransactionStatusEnum.SUCCESS
    assert transaction.paid_at is not None


def test_get_transaction_by_app_trans_id(test_session, sample_booking):
    transaction = create_transaction(booking=sample_booking[0], app_trans_id=f"BOOKING_{sample_booking[0].id}",
                                     payment_url="http://example.com")

    assert get_transaction_by_app_trans_id(app_trans_id=f"BOOKING_{sample_booking[0].id}") == transaction
    assert get_transaction_by_app_trans_id(app_trans_id="1000") is None


def test_get_latest_transaction_by_booking(test_session, sample_booking):
    create_transaction(booking=sample_booking[0], app_trans_id=f"BOOKING_{sample_booking[0].id}_1",
                                     payment_url="http://example.com")

    create_transaction(booking=sample_booking[0], app_trans_id=f"BOOKING_{sample_booking[0].id}_2",
                                     payment_url="http://example.com")
    assert Transaction.query.count() == 2

    transaction = get_latest_transaction_by_booking(booking=sample_booking[0])
    assert transaction.booking_id == sample_booking[0].id
    assert transaction.app_trans_id == f"BOOKING_{sample_booking[0].id}_2"

    transaction = get_latest_transaction_by_booking(booking=sample_booking[1])
    assert transaction is None