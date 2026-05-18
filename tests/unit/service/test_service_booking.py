from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_fields, sample_field_price, sample_field_type, sample_location, sample_address
import pytest
from datetime import date
from werkzeug.exceptions import NotFound
from app.modules.bookings.services import (caculator_total_time, caculator_total_price,
                                           create_booking_service, get_list_booking_service, cancelled_booking_service)


def test_caculator_total_time_service():
    pass


def test_caculator_total_price_service():
    pass


def test_get_list_booking_service():
    pass


def test_create_booking_service():
    pass


def test_cancelled_booking_service():
    pass