from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_field_type, sample_fields
from app.modules.fields.dao import get_list_field_type, get_field_by_id, get_hot_field, get_related_fields
from app.modules.fields.models import FieldStatusEnum


def test_all_field_type(test_session, sample_field_type):
    actual_field_type = get_list_field_type()

    assert actual_field_type[0].name == "Sân bóng 5 người"
    assert len(actual_field_type) == len(sample_field_type)


def test_get_field(test_session, sample_fields):
    field1 = get_field_by_id(field_id = sample_fields[0].id)
    assert field1.name == sample_fields[0].name

    field2 = get_field_by_id(field_id = 10)
    assert field2 is None

    field3 = get_field_by_id(field_id="10")
    assert field3 is None


def test_hot_fields(test_session, sample_fields):
    hot_fields = get_hot_field()

    assert hot_fields != []
    assert len(hot_fields) <= 3
    assert hot_fields[0].id == 1
    assert hot_fields[2].id == 3
    assert len(hot_fields[0].bookings) >= len(hot_fields[1].bookings)
    assert all(f.status == FieldStatusEnum.ACTIVE for f in hot_fields)


def test_related_fields(test_session, sample_fields):
    field_test = get_field_by_id(field_id= sample_fields[0].id)
    related_fields = get_related_fields(field= field_test)

    assert len(related_fields) <= 4
    assert all(f.field_type_id == field_test.field_type_id for f in related_fields)
    assert all(f.status == FieldStatusEnum.ACTIVE for f in related_fields)