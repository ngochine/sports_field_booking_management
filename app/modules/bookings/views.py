from flask import render_template, request
from . import services, dao
from app.common import decorators
from flask_jwt_extended import get_jwt_identity

@decorators.login_required_render
def get_bookings():
    user_id = get_jwt_identity()
    filters = request.args

    res = services.get_list_booking_service(user_id=user_id, filters = filters)

    bookings =  res.get('bookings', None)
    pages = res.get('pages', None)
    page = res.get('page', None)

    return render_template('bookings/bookings.html', bookings= bookings, page=page, pages=pages)
