from . import dao
from app.modules.bookings import dao as booking_dao
import math
from flask import current_app


def get_list_field_service(filters: dict):
    page = filters.get('page', None)
    q = filters.get("q", None)
    field_type_id = filters.get("field_type_id", None)

    fields = dao.load_fields(q=q, field_type_id=field_type_id, page=page)
    field_length = len(fields)
    pages = math.ceil(dao.count_fields(q=q, field_type_id=field_type_id)/current_app.config["PAGE_SIZE"])

    return {
        'fields': fields, 
        'field_length': field_length,
        'pages': pages,
        'page': int(page) if page else 1
    }


def get_field_detail_service(field_id: int):
    field = dao.get_field_by_id(field_id = field_id)
    related_fields = dao.get_related_fields(field = field)
    time_frames = booking_dao.get_list_time_frames_by_field_id(field_id=field_id)

    return {
        'field': field,
        'related_fields': related_fields,
        'time_frames' : time_frames
    }