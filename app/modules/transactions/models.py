from app.extension import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy import Enum as sqlEnum
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from enum import Enum


class TransactionStatusEnum(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class TransactionMethodEnum(Enum):
    ZALOPAY = "zalopay"
    VNPAY = "vnpay"


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(sqlEnum(TransactionMethodEnum), nullable=False)
    status = Column(sqlEnum(TransactionStatusEnum), nullable=False, default=TransactionStatusEnum.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    paid_at = Column(DateTime, nullable=True)
    amount = Column(Numeric(15, 2), nullable=False)
    app_trans_id = Column(String(50), nullable=True)
    payment_url = Column(Text, nullable=True)

    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False, unique=True)
    booking = relationship("Booking", backref=backref("transaction", uselist=False), lazy=True)