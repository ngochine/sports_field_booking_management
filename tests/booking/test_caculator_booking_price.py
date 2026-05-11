from tests.test_base import test_app, test_session, test_client
from datetime import date
from tests.sample_fixtures import sample_fields, sample_field_price


def test_invalid_time(test_client, sample_fields):
    field = sample_fields[0]
    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "12:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Giờ bắt đầu phải sớm hơn giờ kết thúc']}

    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "18:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Giờ bắt đầu phải sớm hơn giờ kết thúc']}


def test_invalid_start_time(test_client, sample_fields):
    field = sample_fields[0]
    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": date.today().isoformat(),
            "end_time": "12:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'start_time': ['Vui lòng chọn giờ bắt đầu']}

    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": date.today().isoformat(),
            "start_time": "99:99",
            "end_time": "18:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'start_time': ['Giờ bắt đầu không hợp lệ']}


def test_invalid_end_time(test_client, sample_fields):
    field = sample_fields[0]
    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": date.today().isoformat(),
            "start_time": "12:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'end_time': ['Vui lòng chọn giờ kết thúc']}

    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "60:01"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'end_time': ['Giờ kết thúc không hợp lệ']}


def test_invalid_booking_date(test_client, sample_fields):
    field = sample_fields[0]
    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'booking_date': ['Vui lòng chọn ngày đặt']}

    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": field.id,
            "booking_date": "22/19/2026",
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'booking_date': ['Ngày đặt không hợp lệ']}


def test_field_not_found(test_client):
    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": 1000,
            "booking_date": date.today().isoformat(),
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ["Sân không tồn tại"]


def test_calculate_price_success(test_client, sample_fields, sample_field_price):
    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": 1,
            "booking_date": "2026-05-11",
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["total_time"] == 2
    assert data["total_price"] == 500000


    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": 1,
            "booking_date": "2026-05-10", #day_of_week
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["total_time"] == 2
    assert data["total_price"] == 700000


    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": 1,
            "booking_date": "2026-04-30",  # special_day
            "start_time": "18:00",
            "end_time": "20:00"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["total_time"] == 2
    assert data["total_price"] == 1000000

    response = test_client.post(
        f"/api/bookings/calculate-price",
        json={
            "field_id": 1,
            "booking_date": "2026-05-11",
            "start_time": "16:00",
            "end_time": "18:30"
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["total_time"] == 2.5
    assert data["total_price"] == 495000