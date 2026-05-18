from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_fields, sample_field_price, sample_field_type, sample_location, sample_address
import pytest
from datetime import date
from werkzeug.exceptions import NotFound
from app.modules.fields.services import get_list_field_service, get_field_detail_service, get_field_prices_service


def test_get_list_field_service(test_session, sample_address, sample_location, sample_field_type, sample_fields):
    result = get_list_field_service(filters={})

    assert len(result["fields"]) == 2
    assert result["field_length"] == 5
    assert result["pages"] == 3
    assert result["page"] == 1

    result = get_list_field_service(
        filters={
            "q": "tennis"
        }
    )

    assert len(result["fields"]) == 1
    assert result["field_length"] == 1

    result = get_list_field_service(
        filters={
            "field_type_id": 1
        }
    )

    assert len(result["fields"]) == 2
    assert result["field_length"] == 3

    result = get_list_field_service(
        filters={
            "province_id": 3
        }
    )

    assert len(result["fields"]) == 2
    assert result["field_length"] == 2

    result = get_list_field_service(
        filters={
            "district_id": 3
        }
    )

    assert len(result["fields"]) == 2
    assert result["field_length"] == 2

    result = get_list_field_service(
        filters={
            "q": "test"
        }
    )

    assert len(result["fields"]) == 0
    assert result["field_length"] == 0
    assert result["pages"] == 0


def test_get_field_detail_service(test_session, sample_address, sample_location, sample_field_type, sample_fields, sample_field_price):
    field = sample_fields[0]

    result = get_field_detail_service(field_id=field.id, date_selected=date(2026, 4, 30))

    assert result["field"].id == field.id
    assert len(result["related_fields"]) == 2
    assert result["field_prices"].count() == 1

    with pytest.raises(NotFound, match="Sân không tồn tại"):
        get_field_detail_service(field_id=999999, date_selected=date.today())


def test_get_field_prices_service(test_session, sample_address, sample_location, sample_field_type, sample_fields, sample_field_price):
    field = sample_fields[0]

    field_prices = get_field_prices_service(
        field_id=field.id, date_selected=date(2026, 4, 30)
    )

    assert field_prices is not None
    assert field_prices.count() == 1
    assert field_prices[0].price == 500000

    field_prices = get_field_prices_service(
        field_id=field.id, date_selected=date(2026, 7, 6)
    )

    assert field_prices.count() == 4

    with pytest.raises(NotFound, match="Sân không tồn tại"):
        get_field_prices_service(field_id=999999, date_selected=date.today())