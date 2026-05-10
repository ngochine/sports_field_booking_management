from .models import Field, FieldType, Location, Address, District, Province
from app.modules.bookings.models import Booking
from flask import current_app
from sqlalchemy import func
from sqlalchemy.orm import joinedload


def load_fields(q = None, field_type_id= None, district_id= None, province_id= None, page= None) -> list[Field]:
    query = Field.query.options(
        joinedload(Field.location)
        .joinedload(Location.address)
        .joinedload(Address.district)
        .joinedload(District.province)
    )

    if q:
        query = query.filter(Field.name.ilike(f"%{q}%"))

    if field_type_id:
        query = query.filter(Field.field_type_id == field_type_id)

    if province_id or district_id:
        query = query.join(Field.location).join(Location.address).join(Address.district)
    if province_id:
        query = query.filter(District.province_id == province_id)
    if district_id:
        query = query.filter(Address.district_id == district_id)

    if page:
        page = int(page)
        start = (page - 1) * current_app.config['PAGE_SIZE']
        query = query.slice(start, start + current_app.config['PAGE_SIZE'])

    return query.all()


def get_list_field_type() -> list[FieldType]:

    return FieldType.query.all()


def get_hot_field() -> list[Field]:
    query = Field.query
    query =query.outerjoin(Booking).group_by(Field.id).order_by(func.count(Booking.id).desc()).limit(3)

    return query.all()


def get_field_by_id(field_id: int) -> Field:
    return Field.query.get(int(field_id))


def get_related_fields(field: Field) -> list[Field]:
    related_fields = Field.query.filter(
        Field.field_type_id == field.field_type_id,
        Field.id != field.id
    ).limit(4).all()
    return related_fields