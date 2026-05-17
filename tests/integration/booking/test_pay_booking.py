from app.modules.bookings.models import BookingStatusEnum
from tests.test_base import test_app, test_session, test_client, test_auth
from tests.sample_fixtures import sample_booking, sample_fields, sample_field_price
from app.modules.auth.models import User, UserStatusEnum, UserRoleEnum
from app.modules.bookings.models import Booking
from datetime import date, timedelta
from app.extension import db


def test_authentication_booking_fail(test_client, sample_booking):
    response = test_client.post(
        "/api/transaction/pay",
        json={
            "booking_id": 1
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
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "07:00",
            "end_time": "09:00"
        }
    )

    booking = response.get_json()["booking"]
    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking.get("id"),
        }
    )
    data = response.get_json()
    print(data)
    assert response.status_code == 200
    assert data["success"] == True
    assert data["payment_url"] != None


def test_authorizer_booking(test_session, test_auth, sample_fields, sample_field_price, sample_booking):
    booking = sample_booking[0]
    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking.id
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == 'Booking không thuộc về bạn, bạn không có quyền thực hiện hành động này'

    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "07:00",
            "end_time": "09:00"
        }
    )
    booking = response.get_json()["booking"]

    user = User.query.first()
    user.status = UserStatusEnum.BANNED
    test_session.commit()

    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking.get("id"),
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
        "/api/transaction/pay",
        json={
            "booking_id": booking.get("id"),
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == "Tài khoản của bạn không đủ quyền để thực hiện hành động này"


def test_not_found_booking(test_auth):
    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": 10000,
        }
    )

    data = response.get_json()
    assert response.status_code == 404
    assert data["success"] == False
    assert data["message"] == "Booking không tồn tại"


def test_expired_booking(test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "07:00",
            "end_time": "09:00"
        }
    )
    booking = Booking.query.get(response.get_json()["booking"]["id"])
    booking.status = BookingStatusEnum.CANCELLED
    db.session.commit()

    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking.id,
        }
    )

    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Booking không ở trạng thái chờ thanh toán']

    booking.status = BookingStatusEnum.PAID
    db.session.commit()

    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking.id,
        }
    )

    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Booking không ở trạng thái chờ thanh toán']


def test_get_payment_url_booking_success(test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "07:00",
            "end_time": "09:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    booking = data["booking"]

    response = test_auth.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking["id"],
        }
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["payment_url"] != None