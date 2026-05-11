import pytest
from tests.test_base import test_session
from app.modules.fields.models import Field, Location, FieldType, Province, District, Address
from app.modules.bookings.models import Booking, FieldPrice
from datetime import date, time


@pytest.fixture
def sample_province(test_session):
    p1 = Province(id=1, name="Hà Nội")
    p2 = Province(id=2, name="Bình Thuận")
    p3 = Province(id=3, name="Thành phố Hồ Chí Minh")

    test_session.add_all([p1, p2, p3])
    test_session.commit()

    return [p1, p2, p3]


@pytest.fixture
def sample_district(test_session):
    d1 = District(id=1, name="Ba Đình", province_id=1)
    d2 = District(id=2, name="Đống Đa", province_id=1)
    d3 = District(id=3, name="Thủ Đức", province_id=3)
    d4 = District(id=4, name="Nhà Bè", province_id=3)
    d5 = District(id=5, name="Quận 2", province_id=3)

    test_session.add_all([d1, d2, d3, d4, d5])
    test_session.commit()

    return [d1, d2, d3, d4, d5]


@pytest.fixture
def sample_address(test_session):
    a1 = Address(street="Đường 1A", district_id=1)
    a2 = Address(street="Đường 2A", district_id=2)
    a3 = Address(street="Đường 3A", district_id=3)
    a4 = Address(street="Đường 4A", district_id=3)

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
    f4 = Field(name="Sân bóng đá 4A", field_type_id=3, location_id=2)
    f5 = Field(name="Sân tennis 5A", field_type_id=1, location_id=3)
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
    fp1 = FieldPrice(start_time=time(6, 0), end_time=time(9, 0), price=150000,
                     day_of_week=None, special_date=None, field_id=1)

    fp2 = FieldPrice(start_time=time(9, 0), end_time=time(17, 0), price=120000,
                     day_of_week=None, special_date=None, field_id=1)

    fp3 = FieldPrice(start_time=time(17, 0), end_time=time(22, 0), price=250000,
                     day_of_week=None, special_date=None, field_id=1)

    fp4 = FieldPrice(start_time=time(6, 0), end_time=time(22, 0), price=300000,
                     day_of_week=5, special_date=None, field_id=1)

    fp5 = FieldPrice(start_time=time(6, 0), end_time=time(22, 0), price=350000,
                     day_of_week=6, special_date=None, field_id=1)

    fp6 = FieldPrice(start_time=time(6, 0), end_time=time(22, 0), price=500000,
                     day_of_week=None, special_date=date(2026, 4, 30), field_id=1)

    test_session.add_all([fp1, fp2, fp3, fp4, fp5, fp6])
    test_session.commit()

    return [fp1, fp2, fp3, fp4, fp5, fp6]
