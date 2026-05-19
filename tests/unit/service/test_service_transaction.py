from app.modules.fields.models import FieldStatusEnum
from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_fields, sample_field_price, sample_booking
import pytest
from datetime import date, time, timedelta, datetime
from werkzeug.exceptions import NotFound, Forbidden
from marshmallow import ValidationError
from app.modules.transactions.services import create_payment_url, handle_payment_callback