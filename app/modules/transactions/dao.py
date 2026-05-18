from app.extension import db
from .models import Transaction, TransactionStatusEnum, TransactionMethodEnum
from app.modules.bookings.models import Booking
from datetime import datetime


def create_transaction(booking: Booking, method = TransactionMethodEnum.VNPAY) -> Transaction:
    transaction = Transaction(
        booking_id=booking.id,
        amount=booking.total_price,
        method=method,
        app_trans_id=f"BOOKING_{booking.id}"
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


def update_transaction(transaction: Transaction, payment_url: str)-> Transaction:
    transaction.payment_url = payment_url
    
    db.session.commit()

    return transaction


def get_transaction_by_id(transaction_id: int) -> Transaction:
    return Transaction.query.get(transaction_id)