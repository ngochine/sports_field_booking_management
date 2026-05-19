from app.extension import db
from .models import Transaction, TransactionStatusEnum, TransactionMethodEnum
from app.modules.bookings.models import Booking
from datetime import datetime


def create_transaction(booking: Booking, app_trans_id:str, payment_url: str, method = TransactionMethodEnum.VNPAY) -> Transaction:
    transaction = Transaction(
        booking_id=booking.id,
        amount=booking.total_price,
        method=method,
        app_trans_id=app_trans_id,
        payment_url = payment_url
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return transaction


def update_transaction_status(transaction: Transaction, status: TransactionStatusEnum) -> Transaction:
    transaction.status = status

    if status == TransactionStatusEnum.SUCCESS:
        transaction.paid_at= datetime.now()

    db.session.commit() 

    return transaction


def get_transaction_by_app_trans_id(app_trans_id: str) -> Transaction:
    return Transaction.query.filter_by(app_trans_id=app_trans_id).first()


def get_transaction_by_id(transaction_id: int) -> Transaction:
    return Transaction.query.get(transaction_id)


def get_latest_transaction_by_booking(booking: Booking) -> Transaction:
    return Transaction.query.filter_by(booking_id=booking.id).order_by(Transaction.created_at.desc()).first()