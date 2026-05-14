from . import dao
from app.modules.bookings import dao as booking_dao
import math
from flask import current_app
from datetime import datetime
from werkzeug.exceptions import NotFound


def get_list_field_service(filters: dict):
    page = filters.get('page', 1)
    q = filters.get("q", None)
    field_type_id = filters.get("field_type_id", None)
    province_id = filters.get("province_id", None)
    district_id = filters.get("district_id", None)

    fields = dao.load_fields(q=q, field_type_id=field_type_id, district_id=district_id, province_id=province_id, page=page)
    field_length = len(dao.load_fields(q=q, field_type_id=field_type_id, district_id=district_id, province_id=province_id))
    pages = math.ceil(field_length/current_app.config["PAGE_SIZE"])

    return {
        'fields': fields, 
        'field_length': field_length,
        'pages': pages,
        'page': int(page) if page else 1
    }


def get_field_detail_service(field_id: int, date_selected: datetime):
    field = dao.get_field_by_id(field_id=field_id)
    if field is None:
        raise NotFound("Sân không tồn tại")
    related_fields = dao.get_related_fields(field=field)
    field_prices = booking_dao.get_field_prices(field=field, date_selected=date_selected)
    
    return {
        'field': field,
        'related_fields': related_fields,
        'field_prices' : field_prices
    }


def get_field_prices_service(field_id: int, date_selected: datetime):
    field = dao.get_field_by_id(field_id=field_id)
    if field is None:
        raise NotFound("Sân không tồn tại")

    field_prices = booking_dao.get_field_prices(field=field, date_selected=date_selected)
    return field_prices