from flask import render_template, request
from . import services, dao
from datetime import date


def get_fields():
    filters = request.args
    res = services.get_list_field_service(filters = filters)

    fields = res.get('fields', None)
    pages = res.get('pages', None)
    page = res.get('page', None)
    field_length = res.get('field_length', 0)
    field_types = dao.get_list_field_type()

    return render_template('fields/fields.html', fields = fields, field_types=field_types, field_length= field_length, pages=pages, page = page)


def get_field_detail(field_id:int):
    res = services.get_field_detail_service(field_id=field_id)
    
    field = res.get('field', None)
    related_fields = res.get('related_fields', None)
    time_frames = res.get('time_frames', None)

    return render_template('fields/field-detail.html', field=field, related_fields=related_fields, time_frames= time_frames, today=date.today().isoformat())