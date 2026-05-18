from flask import render_template, request
from . import services, dao
from flask_jwt_extended import get_jwt_identity


def bookings_view():
    user_id = get_jwt_identity()
    filters = request.args

    res = services.get_list_booking_service(user_id=user_id, filters = filters)

    bookings =  res.get('bookings', None)
    pages = res.get('pages', None)
    page = res.get('page', None)

    return render_template('bookings/bookings.html', bookings= bookings, page=page, pages=pages)


#xử lý quyền, ngoại lệ, last_transaction
def booking_detail_view(booking_id):
    booking = dao.get_booking_by_id(booking_id=booking_id)
    return render_template('bookings/booking-details.html', booking= booking, is_success = None)