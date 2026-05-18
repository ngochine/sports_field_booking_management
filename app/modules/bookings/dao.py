from app.extension import db
from .models import FieldPrice, Booking, BookingStatusEnum
from app.modules.fields.models import Field
from datetime import date, time
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from flask import current_app
from datetime import datetime, date


def query_date_selected(query, date_selected: date):
    weekday = date_selected.weekday()

    special_query = query.filter(
        FieldPrice.special_date == date_selected
    )
    if special_query.first():
        return special_query

    weekday_query = query.filter(
        FieldPrice.day_of_week == weekday
    )
    if weekday_query.first():
        return weekday_query

    default_query = query.filter(
        and_(
            FieldPrice.day_of_week == None,
            FieldPrice.special_date == None
        )
    )
    return default_query


def get_field_prices(field: Field, date_selected= None)-> list[FieldPrice]:
    query = FieldPrice.query.filter_by(field = field)
    if date_selected:
        query = query_date_selected(query, date_selected=date_selected)
    else:
        query = query_date_selected(query, date_selected=date.today())

    return query


def check_booking_overlap(field_id: int, date_selected: date, start_time: time, end_time: time) -> bool:
    query = Booking.query.filter(
        Booking.field_id == field_id,
        Booking.booking_date == date_selected,
        Booking.start_time < end_time, 
        start_time < Booking.end_time)

    return query.first() is not None


def check_booking_limit(user_id: int, booking_date: date) -> bool:
    return Booking.query.filter_by(user_id=user_id, booking_date=booking_date).count() == 3


def create_booking(field_id: int, user_id, total_price: float, data: dict) -> Booking:
    try:
        booking = Booking(
            field_id = field_id,
            user_id = user_id,
            total_price= total_price,
            **data
        )
        db.session.add(booking)
        db.session.commit()
        return booking
    
    except IntegrityError:
        db.session.rollback()
        raise


def get_bookings_by_user(user_id: int, status= None, page=None) -> list[Booking]:
    query = Booking.query.filter_by(user_id=user_id)

    if status:
        if status!="all":
            query = query.filter_by(status=status)

    query = query.order_by(Booking.id.desc())

    if page:
        page = int(page)
        start = (page - 1) * current_app.config['PAGE_SIZE']
        query = query.slice(start, start + current_app.config['PAGE_SIZE'])
    
    return query.all()


def get_booking_by_id(booking_id) -> Booking:
    return Booking.query.get(booking_id)


def update_booking_status(booking: Booking, status: BookingStatusEnum) -> Booking:
    booking.status = status

    db.session.commit()
    return booking


def check_future_booking(field: Field) -> bool:
    now = datetime.now()
    query = Booking.query.filter(Booking.field_id == field.id)
    if query:
        query = query.filter(
            (Booking.booking_date > now.date()) | (Booking.booking_date == now.date()) & (Booking.start_time > now.time())
        )
    return query.first() is not None