from tests.test_base import test_app, test_client


def test_logout_success(test_client):
    test_client.post(
        "/api/auth/register",
        json={
            "username": "test",
            "password": "Abc@123456",
            "confirm": "Abc@123456"
        }
    )
    test_client.post(
        "/api/auth/login",
        json={
            "username": "test",
            "password": "Abc@123456",
        }
    )

    response = test_client.post(
        "/api/auth/logout",
    )
    assert response.status_code == 200

    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie=;" in c for c in cookies)
    assert any("refresh_token_cookie=;" in c for c in cookies)