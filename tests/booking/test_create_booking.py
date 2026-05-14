from app.modules.bookings.models import Booking
from app.modules.fields.models import FieldStatusEnum
from tests.test_base import test_app, test_session, test_client, test_auth
from tests.sample_fixtures import sample_fields, sample_field_price
from app.modules.auth.models import User, UserStatusEnum, UserRoleEnum
from datetime import date, timedelta, datetime


def test_authentication_booking_fail(test_client):
    response = test_client.post(
        "/api/fields/1/booking",
        json={
            "booking_date": "2026-05-11",
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 401
    assert data["success"] == False
    assert data["message"] == "Vui lòng đăng nhập để thực hiện chức năng này"


def test_authentication_booking_success(test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert data["success"] == True
    assert data["booking"] != None


def test_authorizer_booking(test_session, test_auth):
    user = User.query.first()
    user.status = UserStatusEnum.BANNED
    test_session.commit()
    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": "2026-05-11",
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == "Tài khoản của bạn bị cấm nên không thể thực hiện hành động này"


    user.role = UserRoleEnum.ADMIN
    user.status = UserStatusEnum.ACTIVE
    test_session.commit()
    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": "2026-05-11",
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == "Tài khoản của bạn không đủ quyền để thực hiện hành động này"


def test_invalid_start_time(test_auth):
    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": date.today().isoformat(),
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'start_time': ['Vui lòng chọn giờ bắt đầu']}

    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": "26:88",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'start_time': ['Giờ bắt đầu không hợp lệ']}


def test_invalid_end_time(test_auth):
    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'end_time': ['Vui lòng chọn giờ kết thúc']}

    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "78:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'end_time': ['Giờ kết thúc không hợp lệ']}


def test_invalid_booking_date(test_auth):
    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'booking_date': ['Vui lòng chọn ngày đặt sân']}

    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": "2026-76-11",
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'booking_date': ['Ngày đặt không hợp lệ']}

    response = test_auth.post(
        "/api/fields/1/booking",
        json={
            "booking_date": (date.today() - timedelta(days=1)).isoformat(),
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'booking_date': ['Ngày được đặt không được ở quá khứ']}


def test_invalid_time(test_auth, sample_fields):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "12:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Giờ bắt đầu phải sớm hơn giờ kết thúc']}

    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "18:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Giờ bắt đầu phải sớm hơn giờ kết thúc']}

    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=1.5)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Bạn cần đặt ít nhất 1 giờ']}

    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() - timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Giờ bắt đầu phải lớn hơn thời gian hiện tại']}


def test_overlap_schedule(test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=3)).strftime("%H:%M")
        }
    )

    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Khung giờ này đã có người đặt']


def next_weekday():
    d = date.today()
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d + timedelta(days=1)

def test_invalid_field_price(test_auth, sample_fields, sample_field_price):
    field = sample_fields[1]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (next_weekday()).isoformat(),
            "start_time": "07:00",
            "end_time": "11:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"]== ['Khung giờ này chưa được cấu hình giá']


def test_limit_booking(test_auth, test_session, sample_fields, sample_field_price):
    test_auth.post(
        f"/api/fields/{sample_fields[0].id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
        }
    )
    test_auth.post(
        f"/api/fields/{sample_fields[0].id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    response = test_auth.post(
        f"/api/fields/{sample_fields[0].id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=5)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert data["success"] == True
    assert Booking.query.count() == 3

    response = test_auth.post(
        f"/api/fields/{sample_fields[2].id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Tài khoản đã đạt giới hạn đặt trong ngày (3 lần/ngày)']
    assert Booking.query.count() == 3


def test_invalid_field(test_auth, test_session, sample_fields):
    response = test_auth.post(
        f"/api/fields/10000/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 404
    assert data["success"] == False
    assert data["message"] != "Sân không tồn tại"

    field = sample_fields[0]
    field.status = FieldStatusEnum.DELETED
    test_session.commit()
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=3)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 404
    assert data["success"] == False
    assert data["message"] != "Sân không tồn tại"


def test_create_booking_success(test_auth, test_session, sample_fields, sample_field_price):
    field = sample_fields[0]
    test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
        }
    )
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": date.today().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=3)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert data["success"] == True
    assert data["booking"] != None

    assert Booking.query.count() == 2
    assert all(b.field.id == field.id for b in Booking.query.all())