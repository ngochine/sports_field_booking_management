from tests.test_base import test_app, test_client


def test_invalid_input(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )

    response = test_client.post(
        "/api/auth/login",
        json={
            "username": "test"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'password': ['Vui lòng không để trống mật khẩu']}


    response = test_client.post(
        "/api/auth/login",
        json={
            "password": "Abc@123456"
        }
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'username': ['Vui lòng không để trống tên đăng nhập']}


    response = test_client.post(
        "/api/auth/login",
        json={}
    )
    data = response.get_json()
    assert response.status_code == 400
    assert data["success"] == False
    assert data["message"] == {'password': ['Vui lòng không để trống mật khẩu'], 'username': ['Vui lòng không để trống tên đăng nhập']}


def test_not_exist_user(test_client):
    response = test_client.post(
        "/api/auth/login",
        json= {
            "username": "test",
            "password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 401
    assert data["success"] == False
    assert data["message"] == "Sai tài khoản hoặc mật khẩu"


def test_wrong_password(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )

    response = test_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 401
    assert data["success"] == False
    assert data["message"] == "Sai tài khoản hoặc mật khẩu"


def test_set_cookie(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )

    response = test_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "Abc@123456",
        }
    )

    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie" in c for c in cookies)


def test_login_success(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )

    response = test_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "Abc@123456",
        }
    )
    data = response.get_json()
    assert response.status_code == 200
    assert data["success"] == True
    assert data["access_token"] != None
    assert data["refresh_token"] != None
    assert data["user"]["username"] == "test"

    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie" in c for c in cookies)