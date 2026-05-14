import pytest
from tests.test_base import test_session
from app.modules.fields.models import Field, Location, FieldType, Address, FieldStatusEnum
from app.modules.bookings.models import Booking, FieldPrice
from datetime import date, time


@pytest.fixture
def sample_address(test_session):
    a1 = Address(street="Đường 1A", district_id=1, district_name="Ba Đình", province_id=1, province_name="Hà Nội")
    a2 = Address(street="Đường 2A", district_id=2, district_name="Ba Đình", province_id=1, province_name="Hà Nội")
    a3 = Address(street="Đường 3A", district_id=3, district_name="Ba Đình", province_id=3, province_name="Hà Nội")
    a4 = Address(street="Đường 4A", district_id=3, district_name="Ba Đình", province_id=3, province_name="Hà Nội")

    test_session.add_all([a1, a2, a3, a4])
    test_session.commit()

    return [a1, a2, a3, a4]


@pytest.fixture
def sample_location(test_session):
    l1 = Location(name="Trung tâm thể thao 1", address_id=1)
    l2 = Location(name="Trung tâm thể thao 2", address_id=2)
    l3 = Location(name="Trung tâm thể thao 3", address_id=4)
    l4 = Location(name="Trung tâm thể thao 4", address_id=3)

    test_session.add_all([l1, l2, l3, l4])
    test_session.commit()

    return [l1, l2, l3, l4]


@pytest.fixture
def sample_field_type(test_session):
    ft1 = FieldType(name="Sân bóng 5 người", description="Sân bóng 5 người")
    ft2 = FieldType(name="Sân tennis 6 người", description="Sân tennis 6 người")
    ft3 = FieldType(name="Sân bóng 7 người", description="Sân bóng 7 người")
    ft4 = FieldType(name="Sân tennis 5 người", description="Sân tennis 5 người")

    test_session.add_all([ft1, ft2, ft3, ft4])
    test_session.commit()

    return [ft1, ft2, ft3, ft4]


@pytest.fixture
def sample_fields(test_session):
    f1 = Field(name="Sân bóng chuyền", field_type_id=1, location_id=1)
    f2 = Field(name="Sân tennis 2A", field_type_id=2, location_id=1)
    f3 = Field(name="Sân Vận động quốc gia", field_type_id=2, location_id=2)
    f4 = Field(name="Sân bóng đá 4A", field_type_id=3, location_id=2, status=FieldStatusEnum.DELETED)
    f5 = Field(name="Sân tennis 5A", field_type_id=1, location_id=3, status=FieldStatusEnum.DELETED)
    f6 = Field(name="Sân vận động Phú Thọ", field_type_id=1, location_id=3)
    f7 = Field(name="Sân bóng đá 7A", field_type_id=1, location_id=3)

    test_session.add_all([f1, f2, f3, f4, f5, f6, f7])
    test_session.commit()

    return [f1, f2, f3, f4, f5, f6, f7]


@pytest.fixture
def sample_booking(test_session):
    b1 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="PAID",
                 total_price=250000, user_id=1, field_id=1)

    b2 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="PAID",
                 total_price=250000, user_id=1, field_id=2)

    b3 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="PENDING",
                 total_price=250000, user_id=2, field_id=3)

    b4 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="PENDING",
                 total_price=250000, user_id=3, field_id=1)

    b5 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="PAID",
                 total_price=250000, user_id=1, field_id=1)

    b6 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="CANCELLED",
                 total_price=250000, user_id=3, field_id=2)

    b7 = Booking(booking_date=date(2026, 7, 5), start_time=time(18, 30),
                 end_time=time(20, 0), status="CANCELLED",
                 total_price=250000, user_id=3, field_id=4)

    test_session.add_all([b1, b2, b3, b4, b5, b6, b7])
    test_session.commit()

    return [b1, b2, b3, b4, b5, b6, b7]


@pytest.fixture
def sample_field_price(test_session):
    fp1 = FieldPrice(start_time=time(6, 0), end_time=time(12, 0), price=150000,
                     day_of_week=None, special_date=None, field_id=1)

    fp2 = FieldPrice(start_time=time(12, 0), end_time=time(19, 0), price=120000,
                     day_of_week=None, special_date=None, field_id=1)

    fp3 = FieldPrice(start_time=time(19, 0), end_time=time(23, 59), price=250000,
                     day_of_week=None, special_date=None, field_id=1)

    fp4 = FieldPrice(start_time=time(0, 0), end_time=time(6, 0), price=250000,
                     day_of_week=None, special_date=None, field_id=1)

    fp5 = FieldPrice(start_time=time(0, 0), end_time=time(23, 59), price=300000,
                     day_of_week=5, special_date=None, field_id=1)

    fp6 = FieldPrice(start_time=time(0, 0), end_time=time(23, 59), price=350000,
                     day_of_week=6, special_date=None, field_id=1)

    fp7 = FieldPrice(start_time=time(0, 0), end_time=time(23, 59), price=500000,
                     day_of_week=None, special_date=date(2026, 4, 30), field_id=1)

    fp8 = FieldPrice(start_time=time(6, 0), end_time=time(8, 0), price=150000,
                     day_of_week=None, special_date=None, field_id=2)

    fp9 = FieldPrice(start_time=time(11, 0), end_time=time(17, 0), price=120000,
                     day_of_week=None, special_date=None, field_id=2)

    test_session.add_all([fp1, fp2, fp3, fp4, fp5, fp6, fp7, fp8, fp9])
    test_session.commit()

    return [fp1, fp2, fp3, fp4, fp5, fp6, fp7, fp8, fp9]
