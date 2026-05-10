from tests.test_base import test_app, test_session, test_client
from app.modules.auth import services as auth_services
from app.modules.auth.models import User
import pytest
from werkzeug.security import check_password_hash


def test_duplicate_username(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )

    response = test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )

    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Tên người dùng đã tồn tại']


@pytest.mark.parametrize("username", [" "*8, "", "1a"])
def test_invalid_username(test_client, username):
    response = test_client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False


@pytest.mark.parametrize("password", ["1", "1"*8, "a"*8, "1a1"*2, " "*8, "a1A@"*9, "A@1"*3, ""])
def test_invalid_password(test_client, password):
    response = test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": password,
            "confirm": "Abc@123456"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False


def test_invalid_confirm(test_client):
    response = test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "123"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Mật khẩu nhập lại không khớp']}


def test_hash_password(test_session):
    auth_services.register_user(
        {"username": "test",
         "password": "Abc@123456"
         }
    )
    u = User.query.filter(User.username.__eq__("test")).first()

    assert u
    assert u.password != "Abc@123456"
    assert check_password_hash(u.password, "Abc@123456") == True


def test_register_success(test_client):
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