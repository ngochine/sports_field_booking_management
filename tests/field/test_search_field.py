from tests.test_base import test_app, test_session
from tests.sample_fixtures import sample_fields, sample_location, sample_address
from app.modules.fields.dao import load_fields
from app.modules.fields.models import FieldStatusEnum


def test_load_all_fields(sample_fields):
    actual_fields = load_fields()
    active_fields = [
        f for f in sample_fields
        if f.status == FieldStatusEnum.ACTIVE
    ]
    assert len(actual_fields) == len(active_fields)
    assert all(f.status == FieldStatusEnum.ACTIVE for f in actual_fields)


def test_kw(sample_fields):
    actual_field = load_fields(q="Sân vận động")

    assert len(actual_field) == 2
    assert ["Sân vận động" in f.name for f in actual_field]


def test_paging(sample_fields):
    actual_field = load_fields(page=2)
    assert len(actual_field) == 2

    actual_field = load_fields(page=3)
    assert len(actual_field) == 1


def test_field_type(sample_fields):
    actual_field = load_fields(field_type_id=2)
    assert len(actual_field) == 2
    assert [f.field_type_id == 2 for f in actual_field]

    actual_field = load_fields(field_type_id=1)
    assert len(actual_field) == 3
    assert [f.field_type_id == 1 for f in actual_field]

    actual_field = load_fields(field_type_id=4)
    assert len(actual_field) == 0


def test_province_search(sample_fields, sample_address, sample_location):
    actual_field = load_fields(province_id=2)
    assert len(actual_field) == 0

    actual_field = load_fields(province_id=1)
    assert len(actual_field) == 3
    assert [f.location.address.province_id == 1 for f in actual_field]

    actual_field = load_fields(province_id=4)
    assert len(actual_field) == 0


def test_district_search(sample_fields, sample_address, sample_location):
    actual_field = load_fields(district_id=2)
    assert len(actual_field) == 1
    assert [f.location.address.district_id == 2 for f in actual_field]

    actual_field = load_fields(district_id=3)
    assert len(actual_field) == 2
    assert [f.location.address.district_id == 2 for f in actual_field]

    actual_field = load_fields(district_id=4)
    assert len(actual_field) == 0