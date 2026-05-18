from tests.test_base import test_app, test_session, mock_cloudinary
import pytest
from werkzeug.security import check_password_hash
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound
from app.modules.auth.models import User
from app.modules.auth.services import register_user, authenticate_user, update_user_info_service, update_password_service


def test_register_user_service(test_session):
    data = {
        'username': 'test',
        'password': "Abc@123456",
        'confirm': "Abc@123456"
    }
    register_user(validate_data=data)
    user = User.query.filter_by(username='test').first()
    assert check_password_hash(user.password, "Abc@123456")
    assert user.avatar == "https://res.cloudinary.com/dvfuzolim/image/upload/v1768406079/avatar_trang_1_cd729c335b_kitzwg.jpg"

    data = {
        'username': 'test',
        'password': "Abc@123456",
        'confirm': "Abc@123456"
    }
    with pytest.raises(ValidationError, match="Tên người dùng đã tồn tại"):
        register_user(validate_data=data)

    assert User.query.count() == 1


def test_authenticate_user_service(test_session):
    data = {
        'username': 'test',
        'password': "Abc@123456",
        'confirm': "Abc@123456"
    }
    register_user(validate_data=data)

    user = authenticate_user(username='test', password="Abc@123456")
    assert user.username == "test"
    assert check_password_hash(user.password, "Abc@123456")

    user = authenticate_user(username='test', password="Abc")
    assert user == None

    user = authenticate_user(username='test01', password="Abc@123456")
    assert user == None


def test_update_password_service(test_session):
    with pytest.raises(NotFound, match="Không tồn tại người dùng"):
        update_password_service(user_id="1234567", data={})

    data = {
        'username': 'test',
        'password': "Abc@123456",
        'confirm': "Abc@123456"
    }
    user = register_user(validate_data=data)
    assert user.username == "test"

    data_update = {
        'current_password': '1235467',
        'new_password': "Abc@1234",
    }
    with pytest.raises(ValidationError, match="Mật khẩu hiện tại không đúng"):
        update_password_service(data=data_update, user_id=user.id)

    data_update = {
        'current_password': 'Abc@123456',
        'new_password': "Abc@1234",
    }
    update_password_service(data=data_update, user_id=user.id)
    assert user.username == "test"
    assert check_password_hash(user.password, "Abc@1234")
    assert not check_password_hash(user.password, "Abc@123456")


def test_update_user_info_service(test_session, mock_cloudinary):
    with pytest.raises(NotFound, match="Không tồn tại người dùng"):
        update_user_info_service(user_id="1234567", data={})

    data = {
        'username': 'test',
        'password': "Abc@123456",
        'confirm': "Abc@123456"
    }
    user = register_user(validate_data=data)
    assert user.username == "test"

    data_update = {
        "first_name": "test",
        "last_name": "test",
        'email': '123@gmail.com',
        'phone' : "098992077"
    }
    update_user_info_service(data=data_update, avatar="None", user_id=user.id)
    assert user.username == "test"
    assert user.first_name == "test"
    assert user.last_name == "test"
    assert user.avatar == "https://fake-image.png"
    assert user.email == "123@gmail.com"
    assert user.phone == "098992077"