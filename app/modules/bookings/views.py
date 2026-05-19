from flask import render_template, request
from . import services
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, Forbidden


def bookings_view():
    user_id = get_jwt_identity()
    filters = request.args

    res = services.get_list_booking_service(user_id=user_id, filters = filters)

    bookings =  res.get('bookings', None)
    pages = res.get('pages', None)
    page = res.get('page', None)

    return render_template('bookings/bookings.html', bookings= bookings, page=page, pages=pages)


def booking_detail_view(booking_id):
    try:
        res = services.get_booking_detail_service(booking_id=booking_id, user_id=get_jwt_identity())
        booking = res.get('booking', None)
        latest_transaction = res.get('latest_transaction', None)

        return render_template('bookings/booking-details.html', booking= booking,
                               latest_transaction=latest_transaction)

    except ValidationError as e:
        return str(e.messages), 400

    except NotFound as e:
        return str(e.description), 404

    except Forbidden as e:
        return str(e.description), 403

    except Exception as e:
        return str(e), 500