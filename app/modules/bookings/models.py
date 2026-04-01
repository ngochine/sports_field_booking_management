from app.extension import db
from sqlalchemy import Column, Integer, Time, DateTime, Date, ForeignKey, Numeric, Text
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
    ORTHER = "orther"


class TimeFrame(db.Model):
    __tablename__ = 'time_frame'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    price = Column(Numeric(15,2), nullable=False)

    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    field = relationship('Field', backref='time_frames', lazy=True)

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'


class Booking(db.Model):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    booking_date = Column(Date, nullable=False)
    status = Column(sqlEnum(BookingStatusEnum), nullable=False, default=BookingStatusEnum.PENDING)

    time_frame_id = Column(Integer, ForeignKey('time_frame.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)

    time_frame = relationship('TimeFrame', backref='booking')
    user = relationship('User', backref='bookings')
    field = relationship('Field', backref='bookings', lazy=True)


class Report(db.Model):
    __tablename__ = 'report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=True)
    status = Column(sqlEnum(ReportStatusEnum), nullable=False, default=ReportStatusEnum.PENDING)
    tag = Column(sqlEnum(ReportTagEnum), nullable=False, default=ReportTagEnum.INFRASTRUCTURE)

    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    booking = relationship('Booking', backref='reports', lazy=True)
    user = relationship('User', backref='reports', lazy=True)

    def __str__(self):
        return f'{self.booking_id} - {self.tag} - {self.status}'
