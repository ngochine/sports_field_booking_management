from .models import Field, FieldType, Location, Address, District, Province
from app.modules.bookings.models import Booking
from flask import current_app
from sqlalchemy import func
from sqlalchemy.orm import joinedload


def load_fields(q: str, field_type_id: int, district_id: int, province_id: int, page: int) -> list[Field]:
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

    if province_id:
        query = query.join(Field.location).join(Location.address).join(Address.district).filter(District.province_id == province_id)
        if district_id:
            query = query.filter(Address.district_id == district_id)

    if not page:
        page = 1

    if page:
        size = current_app.config["PAGE_SIZE"]
        start = (int(page)-1)*size
        end = start+size
        query = query.slice(start, end)

    return query.all()


def count_fields(q: str, field_type_id: int) -> int:
    query = Field.query
    if q:
        query = query.filter(Field.name.ilike(f"%{q}%"))

    if field_type_id:
        query = query.filter(Field.field_type_id == field_type_id)

    return query.count()


def get_list_field_type() -> list[FieldType]:

    return FieldType.query.all()


def get_hot_field() -> list[Field]:
    query = Field.query
    query =query.outerjoin(Booking).group_by(Field.id).order_by(func.count(Booking.id).desc()).limit(3)

    return query.all()


def get_field_by_id(field_id: int) -> Field:

    return Field.query.get(field_id)


def get_related_fields(field: Field) -> list[Field]:
    related_fields = Field.query.filter(
        Field.field_type_id == field.field_type_id,
        Field.id != field.id
    ).limit(4).all()
    return related_fields