from tests.test_base import test_app, test_session, test_client
from datetime import date, timedelta
from tests.sample_fixtures import sample_fields, sample_field_price


def test_happy_path(test_client, sample_fields, sample_field_price):
    response = test_client.post(
        "/api/auth/register",
        json={
            "username": "demo123",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert data["success"] == True


    response = test_client.post(
        "/api/auth/login",
        json={
            "username": "demo123",
            "password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["user"]["username"] == "demo123"


    field = sample_fields[0]
    response = test_client.post(
        f"/api/fields/{field.id}/booking",
        json={
            "booking_date": (date.today() + timedelta(days=1)).isoformat(),
            "start_time": "10:00",
            "end_time": "12:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert data["success"] == True
    assert data["booking"] != None


    booking = data["booking"]
    response = test_client.post(
        "/api/transaction/pay",
        json={
            "booking_id": booking["id"],
        }
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["payment_url"] != None


    response = test_client.patch(
        f"/api/bookings/{booking["id"]}",
        json={
            "status": "CANCELLED"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["booking"]["status"] == "CANCELLED"


    response = test_client.post(
        "/api/auth/logout",
    )
    assert response.status_code == 200