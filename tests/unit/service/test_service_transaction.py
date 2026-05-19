from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_booking
from app.modules.transactions.models import Transaction, TransactionMethodEnum, TransactionStatusEnum
from app.modules.bookings.models import BookingStatusEnum
import pytest
from datetime import timedelta, datetime
from urllib.parse import urlparse, parse_qs
from werkzeug.exceptions import NotFound, Forbidden
from marshmallow import ValidationError
from app.modules.transactions.services import create_payment_url, handle_payment_callback


def test_create_payment_url_service_fail(test_session, sample_booking):
    with pytest.raises(NotFound, match="Booking không tồn tại"):
        create_payment_url(booking_id=10000, user_id="1", remote_addr="127.0.0.1")

    with pytest.raises(Forbidden, match="Booking không thuộc về bạn, bạn không có quyền thực hiện hành động này"):
        create_payment_url(booking_id=sample_booking[0].id, user_id="2", remote_addr="127.0.0.1")

    with pytest.raises(ValidationError, match="Booking không ở trạng thái chờ thanh toán"):
        booking = sample_booking[0]
        booking.status = BookingStatusEnum.PAID
        test_session.commit()

        create_payment_url(booking_id=sample_booking[0].id, user_id="1", remote_addr="127.0.0.1")

    with pytest.raises(ValidationError, match="Booking không ở trạng thái chờ thanh toán"):
        booking = sample_booking[0]
        booking.status = BookingStatusEnum.CANCELLED
        test_session.commit()

        create_payment_url(booking_id=sample_booking[0].id, user_id="1", remote_addr="127.0.0.1")

    with pytest.raises(ValidationError, match="Đơn hàng đã quá thời hạn 15 phút để thanh toán"):
        booking = sample_booking[0]
        booking.status = BookingStatusEnum.PENDING
        booking.created_at = (datetime.now() - timedelta(minutes=15))
        test_session.commit()

        create_payment_url(booking_id=sample_booking[0].id, user_id="1", remote_addr="127.0.0.1")

    assert Transaction.query.count() == 0


def test_create_payment_url_service_success(test_session, sample_booking):
    booking = sample_booking[0]
    booking.status = BookingStatusEnum.PENDING
    test_session.commit()

    payment_url = create_payment_url(booking_id=booking.id, user_id="1", remote_addr="127.0.0.1")

    assert Transaction.query.count() == 1
    assert payment_url is not None

    parsed_url = urlparse(payment_url)
    assert (parsed_url.scheme== "https")
    assert (parsed_url.netloc == "sandbox.vnpayment.vn")

    query_params = parse_qs(parsed_url.query)
    assert query_params["vnp_Command"] == ["pay"]
    assert query_params["vnp_Amount"] == ["25000000"]
    assert query_params["vnp_CurrCode"] == ["VND"]
    assert query_params["vnp_Locale"] == ["vn"]
    assert query_params["vnp_OrderType"] == ["other"]
    assert query_params["vnp_IpAddr"] == ["127.0.0.1"]

    assert (query_params["vnp_OrderInfo"][0] == "Thanh toan booking 1")

    assert (query_params["vnp_TxnRef"][0].startswith("BOOKING_1_"))

    assert "vnp_CreateDate" in query_params
    assert "vnp_ExpireDate" in query_params
    assert "vnp_SecureHash" in query_params


def test_handle_payment_callback_service_fail(test_session, sample_booking):
    with pytest.raises(NotFound, match="Booking không tồn tại"):
        handle_payment_callback(txn_ref="Booking_10000_abcdef", response_code="00")

    with pytest.raises(NotFound, match="Không tồn tại giao dịch"):
        handle_payment_callback(txn_ref="Booking_1_abcdef", response_code="00")

    assert Transaction.query.count() == 0


def test_handle_payment_callback_service_success(test_session, sample_booking):
    booking = sample_booking[0]
    booking.status = BookingStatusEnum.PENDING
    test_session.commit()

    transaction = Transaction(booking=booking, app_trans_id = f'Booking_1_abcdef', amount= "100000",
                              method= TransactionMethodEnum.VNPAY, payment_url= 'https://example.com')
    test_session.add(transaction)
    test_session.commit()
    assert Transaction.query.count() == 1

    res = handle_payment_callback(txn_ref=transaction.app_trans_id, response_code="00")
    booking = res.get("booking", None)
    assert booking is not None
    assert booking.status == BookingStatusEnum.PAID
    assert transaction.app_trans_id == "Booking_1_abcdef"
    assert transaction.status == TransactionStatusEnum.SUCCESS

    is_success = res.get("is_success", None)
    assert is_success is not None
    assert is_success == True

    booking.status = BookingStatusEnum.PENDING
    test_session.commit()


    res = handle_payment_callback(txn_ref=transaction.app_trans_id, response_code="02")
    booking = res.get("booking", None)
    assert booking is not None
    assert booking.status == BookingStatusEnum.PENDING
    assert transaction.app_trans_id == "Booking_1_abcdef"
    assert transaction.status == TransactionStatusEnum.FAILED

    is_success = res.get("is_success", None)
    assert is_success is not None
    assert is_success == False