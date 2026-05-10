from tests.test_base import test_app, test_session, test_client
from tests.sample_fixtures import sample_fields
from datetime import date
import pytest


@pytest.mark.parametrize("date", [" ", "33/20/2026", "abc", "123", "12/-6/2026"])
def test_invalid_date(test_client, sample_fields, date):
    field = sample_fields[0]
    response = test_client.get(
        f"/api/fields/{field.id}/field-price",
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == "Thiếu ngày để tìm kiếm"


    response = test_client.get(
        f"/api/fields/{field.id}/field-price?date={date}",
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == "Vui lòng nhập đúng định dạng YYYY-MM-DD"


def test_field_not_found(test_client):
    response = test_client.get(
        f"/api/fields/10000/field-price?date={date.today().isoformat()}",
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ["Sân không tồn tại"]


def test_get_field_price_success(test_client, sample_fields):
    field = sample_fields[0]
    response = test_client.get(
        f"/api/fields/{field.id}/field-price?date={date.today().isoformat()}",
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert all([fp.field.id == field.id for fp in data["field_prices"]])