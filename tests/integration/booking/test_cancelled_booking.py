from app.modules.bookings.models import Booking
from tests.test_base import test_app, test_session, test_client, test_auth
from tests.sample_fixtures import sample_booking, sample_fields, sample_field_price
from app.modules.auth.models import User, UserStatusEnum, UserRoleEnum
from datetime import date, timedelta, datetime
import pytest


def test_authentication_cancel_booking_fail(test_client):
    response = test_client.patch(
        "/api/bookings/1",
        json={
            "status": "CANCELLED",
        }
    )
    data = response.get_json()
    assert response.status_code == 401
    assert data["success"] == False
    assert data["message"] == "Vui lòng đăng nhập để thực hiện chức năng này"


def test_authentication_cancel_booking_success(test_auth, test_session, sample_booking):
    user = User.query.first()
    booking = sample_booking[0]
    booking.user_id = user.id
    test_session.commit()

    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
            "status": "CANCELLED",
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["booking"] != None


def test_authorizer_cancel_booking(test_session, test_auth, sample_booking):
    booking = sample_booking[0]

    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
            "status": "CANCELLED",
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == "Booking này không phải của bạn, bạn không có quyền huỷ"


    user = User.query.first()
    user.status = UserStatusEnum.BANNED
    test_session.commit()
    response = test_auth.patch(
        f"/api/bookings/1",
        json={
            "status": "CANCELLED",
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == "Tài khoản của bạn bị cấm nên không thể thực hiện hành động này"


    user.role = UserRoleEnum.ADMIN
    user.status = UserStatusEnum.ACTIVE
    test_session.commit()
    response = test_auth.patch(
        f"/api/bookings/1",
        json={
            "status": "CANCELLED",
        }
    )
    data = response.get_json()
    assert response.status_code == 403
    assert data["success"] == False
    assert data["message"] == "Tài khoản của bạn không đủ quyền để thực hiện hành động này"


@pytest.mark.parametrize("status", ["paid", "pending", "cancelled"])
def test_invalid_data_cancel_booking(test_session, test_auth, sample_booking, status):
    user = User.query.first()
    booking = sample_booking[0]
    booking.user_id = user.id
    test_session.commit()

    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
            "status": status
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {"status": ["Trạng thái huỷ không hợp lệ"]}


def test_invalid_status_cancel_booking(test_session, test_auth, sample_booking):
    user = User.query.first()
    booking = sample_booking[0]
    booking.user_id = user.id
    test_session.commit()
    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
            "status": "PAID"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {"status": ["Chỉ được phép huỷ booking"]}

    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
            "status": "PENDING"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {"status": ["Chỉ được phép huỷ booking"]}

    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {"status": ["Vui lòng cung cấp trạng thái"]}


def test_not_found_booking(test_session, test_auth, sample_booking):
    response = test_auth.patch(
        f"/api/bookings/10000",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 404
    assert data["success"] == False
    assert data["message"] == "Không tồn tại booking"


def test_invalid_booking_status(test_session, test_auth, sample_booking):
    user = User.query.first()
    booking = sample_booking[0]
    booking.user_id = user.id
    booking.status = "CANCELLED"
    test_session.commit()
    response = test_auth.patch(
        f"/api/bookings/{booking.id}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Chỉ được huỷ khi booking có trạng thái PENDING hoặc PAID']


def test_invalid_finish_time_cancel_booking(test_session, test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "07:00",
            "end_time": "09:00"
        }
    )
    assert response.status_code == 201

    booking_id = response.get_json()["booking"]["id"]
    booking = Booking.query.get(booking_id)
    booking.booking_date = (date.today() - timedelta(days=1))
    test_session.commit()

    response = test_auth.patch(
        f"/api/bookings/{booking_id}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ["Không được huỷ booking đã kết thúc"]


def test_invalid_usage_time_cancel_booking(test_session, test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "07:00",
            "end_time": "09:00"
        }
    )
    assert response.status_code == 201

    booking_id = response.get_json()["booking"]["id"]
    booking = Booking.query.get(booking_id)
    booking.booking_date = date.today()
    booking.start_time = (datetime.now()).time()
    booking.end_time = (datetime.now() + timedelta(minutes=60)).time()
    test_session.commit()

    response = test_auth.patch(
        f"/api/bookings/{booking_id}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ["Không được huỷ nếu sân đang trong thời gian sử dụng"]


def test_invalid_time_cancel_booking(test_session, test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today()).isoformat(),
            "start_time": (datetime.now()+ timedelta(hours=1.5)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=2.5)).strftime("%H:%M")
        }
    )
    assert response.status_code == 201

    booking_id = response.get_json()["booking"]["id"]
    booking = Booking.query.get(booking_id)
    booking.start_time =  (datetime.now() + timedelta(hours=1)).time()
    test_session.commit()

    response = test_auth.patch(
        f"/api/bookings/{booking_id}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ["Không được huỷ khi còn dưới 2 giờ trước giờ chơi"]


def test_cancel_booking_pending_success(test_session, test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": (datetime.now() + timedelta(hours=3)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    assert response.status_code == 201
    assert response.get_json()["booking"]["status"] == "PENDING"
    booking_id = response.get_json()["booking"]["id"]

    response = test_auth.patch(
        f"/api/bookings/{booking_id}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["booking"]["status"] == "CANCELLED"


#bổ sung transaction sau
def test_cancel_booking_paid_success(test_session, test_auth, sample_fields, sample_field_price):
    field = sample_fields[0]
    response = test_auth.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": (datetime.now() + timedelta(hours=3)).strftime("%H:%M"),
            "end_time": (datetime.now() + timedelta(hours=4)).strftime("%H:%M")
        }
    )
    assert response.status_code == 201
    booking_id = response.get_json()["booking"]["id"]

    response = test_auth.patch(
        f"/api/bookings/{booking_id}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["booking"]["status"] == "CANCELLED"