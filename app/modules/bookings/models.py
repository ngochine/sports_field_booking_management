from app.extension import db
from sqlalchemy import Column, Integer, Time, DateTime, Date, ForeignKey, Numeric, Text, String
from sqlalchemy import Enum as sqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum


class BookingStatusEnum(Enum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    PAID = "paid"


class ReportStatusEnum(Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    DENIED = "denied"


class ReportTagEnum(Enum):
    INFRASTRUCTURE = "infrastructure"
    FACILITIES = "facilities"
    SERVICE = "service"
    OTHER = "other"


class FieldPrice(db.Model):
    __tablename__ = 'field_price'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    price = Column(Numeric(15,2), nullable=False)
    day_of_week = Column(Integer, nullable=True)
    special_date = Column(Date, nullable=True)

    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    field = relationship('Field', backref='field_price', lazy=True)

    def __str__(self):
        return f'{self.price}'
    
    
class Booking(db.Model):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    booking_date = Column(Date, nullable=False)
    status = Column(sqlEnum(BookingStatusEnum), nullable=False, default=BookingStatusEnum.PENDING)
    total_price = Column(Numeric(15, 2))
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)

    user = relationship('User', backref='bookings')
    field = relationship('Field', backref='bookings', lazy=True)


class Report(db.Model):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=True)
    status = Column(sqlEnum(ReportStatusEnum), nullable=False, default=ReportStatusEnum.PENDING)
    tag = Column(sqlEnum(ReportTagEnum), nullable=False, default=ReportTagEnum.INFRASTRUCTURE)

    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)

    booking = relationship('Booking', backref='reports', lazy=True)
    user = relationship('User', backref='reports', lazy=True)

    def __str__(self):
        return f'{self.booking_id} - {self.tag} - {self.status}'
