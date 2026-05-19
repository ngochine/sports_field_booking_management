from tests.test_base import test_app, test_session, test_auth, test_client, mock_cloudinary
from app.modules.auth import dao as auth_dao
from app.modules.auth.models import User
from app.extension import db
from werkzeug.security import generate_password_hash
import pytest
from io import BytesIO


def test_authentication_update_password_fail(test_client):
    response = test_client.patch(
        "/api/auth/current-user/profile",
        data={
            "first_name": "test",
            "last_name": "test",
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 401
    assert data["success"] == False
    assert data["message"] == "Vui lòng đăng nhập để thực hiện chức năng này"


def test_authentication_update_password_success(test_auth):
    response = test_auth.patch(
        "/api/auth/current-user/profile",
        data={
            "first_name": "test",
            "last_name": "test",
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True


def test_not_exist_user(test_session, test_auth):
    user = User.query.filter_by(username="test").first()

    test_session.delete(user)
    test_session.commit()

    response = test_auth.patch(
        "/api/auth/current-user/profile",
        data={
            "email": "123@gmail.com",
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 404
    assert data["success"] == False
    assert data["message"] == "Không tồn tại người dùng"


@pytest.mark.parametrize("email", ["1@", "abc", "", "@gmail.com"])
def test_invalid_email_update_user_profile(test_auth, email):
    response = test_auth.patch(
        "/api/auth/current-user/profile",
        data={
            "email": email,
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False


@pytest.mark.parametrize("phone", ["090909", "", "12345678990", "abcdefghtg", "1234 56790"])
def test_invalid_phone_update_user_profile(test_auth, phone):
    response = test_auth.patch(
        "/api/auth/current-user/profile",
        data={
            "phone": phone,
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False


def test_duplicated_email_update_user_profile(test_auth):
    data = {"username": "test2", "email": "test@gmail.com"}
    auth_dao.create_new_user(generate_password_hash("Abc@123456"), **data)

    response = test_auth.patch(
        "/api/auth/current-user/profile",
        data={
            "email": "test@gmail.com",
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == "Email đã được đăng ký"


def test_change_user_profile_success(test_auth, mock_cloudinary):
    response = test_auth.patch(
        "/api/auth/current-user/profile",
        data={
            "first_name": "test",
            "last_name": "test",
            "avatar": (
                BytesIO(b"fake image"),
                "avatar.png"
            ),
            "phone": "0998992077",
            "email": "abc@gmail.com",
        },
        content_type="multipart/form-data"
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["user"]["first_name"] == "test"
    assert data["user"]["last_name"] == "test"
    assert data["user"]["email"] == "abc@gmail.com"
    assert data["user"]["avatar"] == "https://fake-image.png"