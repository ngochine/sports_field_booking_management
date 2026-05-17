from tests.test_base import test_app, test_session, test_auth, test_client
from app.modules.auth.models import User
from app.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
import pytest


def test_authentication_update_password_fail(test_client):
    response = test_client.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "new_password": "Abc@123456",
            "confirm_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 401
    assert data["success"] == False
    assert data["message"] == "Vui lòng đăng nhập để thực hiện chức năng này"


def test_authentication_update_password_success(test_auth):
    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "new_password": "Abc@123456",
            "confirm_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True


def test_not_exist_user(test_auth):
    user = User.query.filter_by(username="test").first()

    db.session.delete(user)
    db.session.commit()

    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "new_password": "Abc@1234",
            "confirm_password": "Abc@1234",
        }
    )
    data = response.get_json()
    print(data)
    assert response.status_code == 404
    assert data["success"] == False
    assert data["message"] == "Không tồn tại người dùng"


def test_invalid_input_change_password(test_auth):
    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "new_password": "Abc@123456",
            "confirm_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'current_password': ['Vui lòng không để trống mật khẩu hiện tại']}

    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "confirm_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'new_password': ['Vui lòng không để trống mật khẩu mới']}

    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "new_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'confirm_password': ['Vui lòng không để trống xác nhận']}


def test_invalid_confirm_password(test_auth):
    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "new_password": "Abc@123456",
            "confirm_password": "Abc",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'_schema': ['Mật khẩu nhập lại không khớp']}


def test_invalid_current_password(test_auth, test_session):
    user = User.query.first()
    user.password = generate_password_hash("123456Abc@")
    test_session.commit()

    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": "Abc@123456",
            "new_password": "Abc@123456",
            "confirm_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == ['Mật khẩu hiện tại không đúng']


@pytest.mark.parametrize("new_password", ["1", "1"*8, "a"*8, "1a1"*2, " "*8, "a1A@"*9, "A@1"*3, "abc123@n", "abv123VB"])
def test_invalid_new_password(test_auth, test_session, new_password):
    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": 'Abc@123456',
            "new_password": new_password,
            "confirm_password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False


def test_change_password_success(test_auth, test_client):
    response = test_auth.patch(
        "/api/auth/current-user/change-password",
        json={
            "current_password": 'Abc@123456',
            "new_password": "Test123@",
            "confirm_password": "Test123@",
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True

    user = User.query.first()
    assert check_password_hash(user.password, "Test123@") == True
    assert check_password_hash(user.password, "Abc@123456") == False


    response = test_client.post(
        "/api/auth/logout",
    )
    assert response.status_code == 200

    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie=;" in c for c in cookies)


    response = test_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "Test123@",
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["access_token"] != None
    assert data["refresh_token"] != None