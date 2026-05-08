from app.extension import db
from .models import FieldPrice, Booking
from app.modules.fields.models import Field
from datetime import date, time
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError


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


def get_field_prices(field: Field, date_selected: date)-> list[FieldPrice]:
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
