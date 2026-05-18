from flask import Blueprint
from . import views, apis
from app.common import decorators

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/bookings', methods=["GET"])
@decorators.customer_required_render
def bookings():
    return views.bookings_view()


@booking_bp.route('/bookings/<int:booking_id>', methods=["GET"])
@decorators.customer_required_render
def booking_detail(booking_id):
    return views.booking_detail_view(booking_id)


# API
api_booking_bp = Blueprint('api_booking', __name__, url_prefix='/api')

@api_booking_bp.route('/bookings/calculate-price', methods=['POST'])
def calculate_price():
    return apis.calculate_price_api()


@api_booking_bp.route('/bookings/<int:booking_id>', methods=['PATCH'])
@decorators.customer_required_api
def cancelled_booking(booking_id):
    return apis.cancelled_booking_api(booking_id)
