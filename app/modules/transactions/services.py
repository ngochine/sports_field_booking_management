import hashlib
import hmac
import urllib.parse
from flask import current_app
from app.modules.bookings import dao as booking_dao
from app.modules.bookings.models import Booking, BookingStatusEnum
from . import dao
from .models import TransactionStatusEnum
from werkzeug.exceptions import NotFound, Forbidden
from marshmallow.exceptions import ValidationError
from datetime import datetime, timedelta
import uuid
from app.common.tasks import trigger_task, task_auto_update_transaction_status


def validate_create_payment_url(booking: Booking, user_id: str):
    if booking is None:
        raise NotFound("Booking không tồn tại")

    if booking.user_id != user_id:
        raise Forbidden("Booking không thuộc về bạn, bạn không có quyền thực hiện hành động này")

    if booking.status != BookingStatusEnum.PENDING:
        raise ValidationError("Booking không ở trạng thái chờ thanh toán")
    
    if datetime.now() > (booking.created_at + timedelta(minutes=15)):
        raise ValidationError("Đơn hàng đã quá thời hạn 15 phút để thanh toán")


def create_payment_url(booking_id: int, user_id: str, remote_addr: str) -> str:
    booking = booking_dao.get_booking_by_id(booking_id)
    validate_create_payment_url(booking= booking, user_id=user_id)

    app_trans_id = f"BOOKING_{booking.id}_{uuid.uuid4().hex[:10]}"
    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": current_app.config['VNP_TMN_CODE'],
        "vnp_Amount": str(int(booking.total_price)*100),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": app_trans_id,
        "vnp_OrderInfo": f"Thanh toan booking {booking.id}",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": current_app.config['VNP_RETURN_URL'],
        "vnp_IpAddr": remote_addr,
        "vnp_CreateDate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "vnp_ExpireDate": (booking.created_at + timedelta(minutes=15)).strftime('%Y%m%d%H%M%S')
    }
    params = {
        k: v for k, v in params.items()
        if v is not None and v != ""
    }

    sorted_params = sorted(params.items())
    hash_data = "&".join(
        [
            f"{k}={urllib.parse.quote_plus(str(v))}"
            for k, v in sorted_params
        ]
    )

    secure_hash = hmac.new(
        current_app.config["VNP_SECRET_KEY"].encode("utf-8"),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    query_string = urllib.parse.urlencode(sorted_params)

    payment_url = f"{current_app.config['VNP_URL']}?{query_string}&vnp_SecureHash={secure_hash}"

    transaction = dao.create_transaction(booking=booking, app_trans_id= app_trans_id, payment_url= payment_url)
    trigger_task(func=task_auto_update_transaction_status, run_date=(transaction.created_at + timedelta(minutes=15)),
                 args=[transaction.id])

    return transaction.payment_url


def handle_payment_callback(txn_ref, response_code) -> dict:
    booking_id = txn_ref.split("_")[1]
    booking = booking_dao.get_booking_by_id(booking_id)

    if booking is None:
        raise NotFound("Booking không tồn tại")

    transaction = dao.get_transaction_by_app_trans_id(app_trans_id=txn_ref)
    if transaction is None:
        raise NotFound("Không tồn tại giao dịch")

    if response_code == "00":
        booking = booking_dao.update_booking_status(booking=booking, status=BookingStatusEnum.PAID)
        dao.update_transaction_status(transaction= transaction, status=TransactionStatusEnum.SUCCESS)
        is_success = True
    else:
        dao.update_transaction_status(transaction=transaction, status=TransactionStatusEnum.FAILED)
        is_success = False
        
    return {
        "booking": booking,
        "is_success": is_success
    }